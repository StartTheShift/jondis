
import unittest
from jondis.tests.manager import Manager


class BaseJondisTest(unittest.TestCase):
    def setUp(self):
        self.manager = Manager()
        self.start()

    def start(self):
        """
        We always need to run the base setup, so we might as well just call start() instead
        of using super() on every single test.  Slightly less obnoxious
        """
        raise NotImplementedError("You must use the start() method to start redis servers.")

    def tearDown(self):
        self.manager.shutdown()
