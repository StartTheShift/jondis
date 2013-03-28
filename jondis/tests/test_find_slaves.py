
from jondis.tests.base import BaseJondisTest
from jondis.pool import Pool


class BasicFindSlavesTest(BaseJondisTest):
    def start(self):
        self.master = self.manager.start('master')
        self.slave = self.manager.start('slave', self.master)

    def test_update_hosts(self):
        """
        ensures the self.pool is aware of the slaves after updating
        """
        hosts = ['127.0.0.1:{}'.format(self.master),
                 '127.0.0.1:{}'.format(self.slave)]

        pool = Pool(hosts=hosts)

        assert len(pool._slave_pool) == 1
        assert len(pool._master_pool) == 1

class DiscoverSlavesTest(BaseJondisTest):

    def start(self):
        self.master = self.manager.start('master')
        self.slave = self.manager.start('slave', self.master)
        self.slave2 = self.manager.start('slave2', self.master)

    def test_find_slave(self):
        # tests that we auto discover the 2nd slave
        hosts = ['127.0.0.1:{}'.format(self.master),
                 '127.0.0.1:{}'.format(self.slave)]

        pool = Pool(hosts=hosts)

        assert len(pool._hosts) == 3, pool._hosts
        assert len(pool._slave_pool) == 2
        assert len(pool._master_pool) == 1

class SlaveDiscovery2Test(BaseJondisTest):
    def start(self):
        self.master = self.manager.start('master')
        self.slave = self.manager.start('slave', self.master)
        self.slave2 = self.manager.start('slave2', self.master)

        hosts = ['127.0.0.1:{}'.format(self.master)]

        self.pool = Pool(hosts=hosts)

    def test_update_hosts(self):
        """
        ensures the self.pool is aware of the slaves after updating
        """

        assert len(self.pool._hosts) == 3, self.pool._hosts
        assert len(self.pool._slave_pool) == 2
        assert len(self.pool._master_pool) == 1
