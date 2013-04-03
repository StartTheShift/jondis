from Queue import Queue
from itertools import chain
import os
from redis import ConnectionError
from redis.connection import Connection
from redis.client import parse_info
from collections import namedtuple
import logging
import socket

logger = logging.getLogger(__name__)

Server = namedtuple('Server', ['host', 'port'])


class Pool(object):

    def __init__(self, connection_class=Connection,
                 max_connections=None, hosts=[],
                 **connection_kwargs):

        self.pid = os.getpid()
        self.connection_class = connection_class
        self.connection_kwargs = connection_kwargs
        self.max_connections = max_connections or 2 ** 31
        self._in_use_connections = set()

        self._hosts = set() # current active known hosts
        self._current_master = None # (host,port)

        self._master_pool = set()
        self._slave_pool = set()
        self._created_connections = 0

        for x in hosts:
            if ":" in x:
                (host, port) = x.split(":")

            else:
                host = x
                port = 6379
            host = socket.gethostbyname(host)
            self._hosts.add(Server(host, int(port)))

        self._configure()

    def _configure(self):
        """
        given the servers we know about, find the current master
        once we have the master, find all the slaves
        """
        logger.debug("Running configure")
        to_check = Queue()
        for x in self._hosts:
            to_check.put(x)

        while not to_check.empty():
            x = to_check.get()

            try:
                conn = self.connection_class(host=x.host, port=x.port, **self.connection_kwargs)
                conn.send_command("INFO")
                info = parse_info(conn.read_response())

                if info['role'] == 'slave':
                    self._slave_pool.add(conn)
                elif info['role'] == 'master':
                    self._current_master = x
                    logger.debug("Current master {}:{}".format(x.host, x.port))
                    self._master_pool.add(conn)
                    slaves = filter(lambda x: x[0:5] == 'slave', info.keys())
                    slaves = [info[y] for y in slaves]
                    slaves = [y.split(',') for y in slaves]
                    slaves = filter(lambda x: x[2] == 'online', slaves)
                    slaves = [Server(x[0], int(x[1])) for x in slaves]

                    for y in slaves:
                        if y not in self._hosts:
                            self._hosts.add(y)
                            to_check.put(y)

                    # add the slaves
            except:
                # remove from list
                to_remove = []
        logger.debug("Configure complete, host list: {}".format(self._hosts))


    def _checkpid(self):
        if self.pid != os.getpid():
            self.disconnect()
            self.__init__(self.connection_class, self.max_connections,
                          **self.connection_kwargs)

    def get_connection(self, command_name, *keys, **options):
        "Get a connection from the pool"
        self._checkpid()
        try:
            connection = self._master_pool.pop()
            logger.debug("Using connection from pool")
        except KeyError:
            logger.debug("Creating new connection")
            connection = self.make_connection()

        self._in_use_connections.add(connection)
        return connection

    def make_connection(self):
        "Create a new connection"
        if self._created_connections >= self.max_connections:
            raise ConnectionError("Too many connections")

        self._created_connections += 1

        if self._current_master == None:
            logger.debug("No master set - reconfiguratin")
            self._configure()

        host = self._current_master[0]
        port = self._current_master[1]

        logger.debug("Creating new connection to {}:{}".format(host, port))
        return self.connection_class(host=host, port=port, **self.connection_kwargs)

    def release(self, connection):

        """
        Releases the connection back to the pool
        if the connection is dead, we disconnect all
        """

        if connection._sock is None:
            logger.debug("Dead socket, reconfigure")
            self.disconnect()
            self._configure()
            self._current_master = None
            server = Server(connection.host, int(connection.port))
            self._hosts.remove(server)
            logger.debug("New configuration: {}".format(self._hosts))

            return

        self._checkpid()
        if connection.pid == self.pid:
            self._in_use_connections.remove(connection)
            self._master_pool.add(connection)

    def disconnect(self):
        "Disconnects all connections in the pool"
        self._master_pool = set()
        self._slave_pool = set()
        self._in_use_connections = set()


