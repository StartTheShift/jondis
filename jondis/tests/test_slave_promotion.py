from jondis.pool import Pool
from jondis.tests.base import BaseJondisTest
import redis

class SlavePromotionTest(BaseJondisTest):
    def start(self):
        self.master = self.manager.start('master')
        self.slave = self.manager.start('slave', self.master)

        assert self.master > 0
        assert self.slave > 0


    def test_promotion(self):
        pool = Pool(hosts=['127.0.0.1:{}'.format(self.master)])
        r = redis.StrictRedis(connection_pool=pool)

        tmp = r.set('test', 1)
        tmp2 = r.get('test2')



