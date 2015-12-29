# coding=utf-8
"""
Tests module for classes' instances
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

    @classmethod
    def setUpClass(cls):
        cls.agent = Agent(cls.tests[0][0], cls.tests[0][1])
        cls.orders_book = OrdersBook(cls.agent)
        cls.order = Order(cls.orders_book)

    def test_should_create_agent(self):
        agent = self.agent
        print(agent)
        assert agent.account == self.tests[0][0]
        assert agent.venue == self.tests[0][1]

    def test_should_create_orders_book(self):
        orders_book = self.orders_book
        print(orders_book)

    def test_should_create_order(self):
        order = self.order
        print(order)
        assert order.agent == self.agent
        assert order.account == self.agent.account
        assert order.venue == self.agent.venue

    @classmethod
    def tearDownClass(cls):
        del cls


def suite():
    s = unittest.TestSuite()
    s.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(Test_Agent_Order))
    return s


if __name__ == "__main__":
    t = unittest.TextTestRunner()
    t.run(suite())

