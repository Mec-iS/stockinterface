# coding=utf-8
"""
Unit Tests module for Endpoints' URLs fetching
"""
import unittest
from unittest import mock

__author__ = 'Lorenzo'


# (account, venue, stock)
tests = [
    ('YCH86804436', 'SSDX', 'PMI'),
    ('WCF86833536', 'CDKX', 'FRI'),
    ('RTS86811456', 'DTEX', 'RTY')
]

from endpoints import APIHeartBeat
from client import _request, _response
class Test_Enpoint_APIHeartBeat(unittest.TestCase):
    def setUp(self):
        self.endpoint = APIHeartBeat()

    def test_should_create_endpoint(self):
        print(self.endpoint)
        assert isinstance(self.endpoint, APIHeartBeat)
        assert self.endpoint.url == 'https://api.stockfighter.io/ob/api/heartbeat'

    def test_should_fetch_endpoint(self):
        print('>>> heartbeating')
        body, _ = _response(_request(self.endpoint.url))
        print('>>> response: ' + str(body))
        assert body["ok"]

    def tearDown(self):
        del self.endpoint


from endpoints import VenueHeartBeat
class Test_Enpoint_VenueHeartBeat(unittest.TestCase):
    tests = tests

    def setUp(self):
        self.endpoint = VenueHeartBeat(tests[0][1])

    def test_should_create_endpoint(self):
        print(self.endpoint)
        assert isinstance(self.endpoint, VenueHeartBeat)
        assert self.endpoint.url == 'https://api.stockfighter.io/ob/api/venues/SSDX/heartbeat'

    def tearDown(self):
        del self.endpoint


from endpoints import Stocks
class Test_Enpoint_Stocks(unittest.TestCase):
    tests = tests

    def setUp(self):
        self.endpoint = Stocks(
            venue=tests[0][1],
            stock=tests[0][2]
        )

    def test_should_create_endpoint(self):
        assert self.endpoint.venue == tests[0][1] and self.endpoint.stock == tests[0][2]
        assert all(getattr(self.endpoint, v[0], None) for v in self.endpoint.actions)
        print(self.endpoint)

    def tearDown(self):
        del self.endpoint


def suite():
    s = unittest.TestSuite()
    s.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(Test_Enpoint_APIHeartBeat))
    s.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(Test_Enpoint_VenueHeartBeat))
    s.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(Test_Enpoint_Stocks))
    return s


if __name__ == "__main__":
    t = unittest.TextTestRunner()
    t.run(suite())
