
from jondis.tests.base import BaseJondisTest
from jondis.pool import Pool


class FindSlavesTest(BaseJondisTest):
    def start(self):
        self.master = self.manager.start('master')
        self.slave = self.manager.start('slave')
        hosts = ['localhost:{}'.format(self.master),
                 'localhost:{}'.format(self.slave)]

        self.pool = Pool(hosts=hosts)

    def test_update_hosts(self):
        """
        ensures the self.pool is aware of the slaves after updating
        """

        assert len(self.pool._slave_pool) == 1
        assert len(self.pool._master_pool) == 1

