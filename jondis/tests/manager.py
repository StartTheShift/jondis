
import subprocess
import os

# im picking an arbitarily high port
# starting point, going up from here
from time import sleep
import redis
import logging

logger = logging.getLogger(__name__)

port = 25530
DEVNULL=open(os.devnull, 'wb')

class Manager(object):
    def __init__(self):
        # procs is a dict of tuples (proc, port)
        self.procs = {}

    def start(self, name, master=None):
        """
        :type master int
        """
        global port
        slave_of = "--slaveof 127.0.0.1 {}".format(master) if master else ""

        start_command = "redis-server --port {} {}".format(port, slave_of)

        proc = subprocess.Popen(start_command, shell=True, stdout=DEVNULL, stderr=DEVNULL)

        self.procs[name] = (proc, port)
        port += 1
        # ghetto hack but necessary to find the right slaves
        sleep(.1)
        return self.procs[name][1]

    def stop(self, name):
        (proc, port) = self.procs[name]
        proc.terminate()
        # same hack as above to make sure failure actually happens
        sleep(.1)

    def promote(self, port):
        admin_conn = redis.StrictRedis('localhost', port)
        logger.debug("Promoting {}".format(port))
        admin_conn.slaveof() # makes it the master
        sleep(.1)

    def shutdown(self):
        for (proc,port) in self.procs.itervalues():
            proc.terminate()

    def __getitem__(self, item):
        return self.procs[item]



