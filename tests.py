# coding=utf-8
"""
Unit Tests module
"""
import unittest
__author__ = 'Lorenzo'


class Test_API_uptime(unittest.TestCase):
    def setUp(self):
        from apimodels import HeartBeat
        self.response = HeartBeat.check_if_api_is_up()

    def test_should_heartbeat_the_api(self):
        print(self.response)
        if not self.response["ok"]:
            assert False
        assert True

    def tearDown(self):
        del self.response


def suite():
    s = unittest.TestSuite()
    s.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(Test_API_uptime))
    return s

# The typical main program for a test module.
# ::

if __name__ == "__main__":
    t = unittest.TextTestRunner()
    t.run(suite())