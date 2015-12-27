# coding=utf-8
"""
Unit Tests module for Endpoints' URLs fetching
"""
import unittest
import asyncio
__author__ = 'Lorenzo'


class Test_API(unittest.TestCase):
    def setUp(self):
        from endpoints import APIHeartBeat
        self.endpoint = APIHeartBeat()

    def test_the_api_should_heartbeat(self):
        self.endpoint._get()
        if not self.endpoint.response["ok"]:
            assert False
        assert True

    def tearDown(self):
        del self.endpoint


class Test_Venue(unittest.TestCase):
    test = ['CDKEX']

    def setUp(self):
        from endpoints import VenueHeartBeat
        self.endpoint = VenueHeartBeat(self.test[0])

    def test_the_api_should_heartbeat(self):
        self.endpoint._get()
        if not self.endpoint.response["ok"]:
            assert False
        assert True

    def tearDown(self):
        del self.endpoint


def suite():
    s = unittest.TestSuite()
    s.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(Test_API))
    s.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(Test_Venue))
    return s

# The typical main program for a test module.
# ::

if __name__ == "__main__":
    t = unittest.TextTestRunner()
    t.run(suite())