
import unittest
from jondis.tests.manager import Manager


class BaseJondisTest(unittest.TestCase):
    def setUp(self):
        self.manager = Manager()
        self.start()

    def tearDown(self):
        self.manager.shutdown()
