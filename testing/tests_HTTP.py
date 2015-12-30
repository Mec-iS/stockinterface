# coding=utf-8
"""
Unit Tests module for Endpoints' URLs fetching
"""
import sys
import unittest
from unittest import mock

from endpoints import APIHeartBeat, VenueHeartBeat, Stocks
from client import _request, _response
from play import Play

__author__ = 'Lorenzo'


# (account, venue, stock)
tests = [
    ('YCH86804436', 'SSDX', 'PMI'),
    ('WCF86833536', 'CDKX', 'FRI'),
    ('RTS86811456', 'DTEX', 'RTY')
]


class Test:
    def __init__(self, account, venue, stock):
        self.account = account
        self.venue = venue
        self.stock = stock


class Test_Enpoint_APIHeartBeat(unittest.TestCase):
    def setUp(self):
        self.endpoint = APIHeartBeat()

    def test_should_create_endpoint(self):
        print(self.endpoint)
        self.assertIsInstance(self.endpoint, APIHeartBeat)
        self.assertEqual(self.endpoint.url, 'https://api.stockfighter.io/ob/api/heartbeat')

    def test_should_fetch_endpoint(self):
        print('>>> heartbeating')
        body, _ = _response(_request(self.endpoint.url))
        print('>>> response: ' + str(body))
        self.assertTrue(body["ok"])

    def tearDown(self):
        del self.endpoint


class Test_Enpoint_VenueHeartBeat(unittest.TestCase):
    def setUp(self):
        self.t = Test(sys.argv[1],
            sys.argv[2],
            sys.argv[3]
        )

        self.endpoint = VenueHeartBeat(self.t.venue)

    def test_should_create_endpoint(self):
        print(self.endpoint)
        self.assertIsInstance(self.endpoint, VenueHeartBeat)
        self.assertEqual(
            self.endpoint.url,
            'https://api.stockfighter.io/ob/api/venues/{}/heartbeat'.format(self.t.venue)
        )

    def tearDown(self):
        del self.endpoint


class Test_Enpoint_Stocks(unittest.TestCase):
    def setUp(self):
        self.t = Test(
            sys.argv[1],
            sys.argv[2],
            sys.argv[3]
        )
        self.venue = self.t.venue
        self.stock = self.t.stock
        self.endpoint = Stocks(
            venue=self.t.venue,
            stock=self.t.stock
        )

    def test_should_create_endpoint(self):
        self.assertTrue(self.endpoint.venue == self.venue and self.endpoint.stock == self.stock)
        self.assertTrue(all(getattr(self.endpoint, v[0], None) for v in self.endpoint.actions))
        print(self.endpoint)

    def test_should_return_orders_by_stock(self):
        Play.dispatch(
            caller=None,
            url=self.endpoint.orders_by_stock
        )

    def test_should_return_quote_for_a_stock(self):
        Play.dispatch(None, self.endpoint.orders_by_stock)

    def tearDown(self):
        del self.endpoint


def suite(**kwargs):
    s = unittest.TestSuite()
    s.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(Test_Enpoint_APIHeartBeat))
    s.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(
        Test_Enpoint_VenueHeartBeat
    ))
    s.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(
        Test_Enpoint_Stocks
    ))
    return s


if __name__ == "__main__":
    t = unittest.TextTestRunner()
    t.run(suite())
