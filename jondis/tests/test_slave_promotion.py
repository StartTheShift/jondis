from jondis.tests.base import BaseJondisTest


class SlavePromotionTest(BaseJondisTest):
    def start(self):
        self.master = self.manager.start('master')
        assert self.master > 0
        self.slave = self.manager.start('slave', self.master)
        assert self.slave > 0

    def test_get_info(self):
        pass

