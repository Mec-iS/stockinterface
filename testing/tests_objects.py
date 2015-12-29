# coding=utf-8
"""
Tests module for classes' instances
"""
import unittest
from unittest import mock

__author__ = 'Lorenzo'


global play_loop
# (account, venue, stock)
tests = [
    ('YCH86804436', 'SSDX', 'PMI'),
    ('WCF86833536', 'CDKX', 'FRI'),
    ('RTS86811456', 'DTEX', 'RTY')
]

from game import Agent, OrdersBook, Order
class Test_Agent_Order(unittest.TestCase):
    tests = tests
    fake_order = {
        "stock": tests[0][2],
        "price": 5467,
        "qty": 1000,
        "direction": "buy",
        "orderType": "limit"
    }

    def setUp(self):
        self.agent = agent =  Agent(self.tests[0][0], self.tests[0][1])
        self.orders_book = orders_book = OrdersBook(agent)
        self.order = Order(orders_book)

    def test_should_create_agent(self):
        print(self.agent)
        assert self.agent.account == self.tests[0][0]
        assert self.agent.venue == self.tests[0][1]

    def test_should_create_order(self):
        print(self.order)
        assert self.order.agent == self.agent
        assert self.order.account == self.agent.account
        assert self.order.venue == self.agent.venue

    def tearDown(self):
        del self.agent
        del self.order


from endpoints import APIHeartBeat
class Test_Enpoint_APIHeartBeat(unittest.TestCase):
    def setUp(self):

        self.endpoint = APIHeartBeat()

    def test_should_create_endpoint(self):
        print(self.endpoint)
        assert isinstance(self.endpoint, APIHeartBeat)
        assert self.endpoint.url == 'https://api.stockfighter.io/ob/api/heartbeat'

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
    s.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(Test_Agent_Order))
    s.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(Test_Enpoint_APIHeartBeat))
    s.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(Test_Enpoint_VenueHeartBeat))
    s.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(Test_Enpoint_Stocks))
    return s


if __name__ == "__main__":
    t = unittest.TextTestRunner()
    t.run(suite())

