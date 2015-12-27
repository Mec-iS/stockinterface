# coding=utf-8
"""
Module collecting simple tasks
"""
import json
from endpoints import VenueOrderBook
from levels import Level

__author__ = 'Lorenzo'


class Dispatch:
    """
    Simple or complex actions to be performed on the market, with needed method
    to be dispatched to the market.
    """
    params = ('loop', 'order', 'endpoint', )

    def __init__(self, loop, order, endpoint):
        self.loop = loop          # from Play.start_play_loop()
        self.order = order        # from game.Order
        self.endpoint = endpoint  # from Endpoint.{appropriate endpoint}

    def __repr__(self):
        return "Disparcher-{id!r} is dispatching {order!r} using {loop!r}".format(
            id=id(self),
            order=self.order.__repr__(),
            loop=self.loop.__repr__()
        )

    def __str__(self):
        return "Disparcher: {id!r}".format(id=id(self))

    def get(self, caller, mode):
        """

        :param Endpoint caller:
        :param str mode:
        :return:
        """
        response = yield from self.loop.create_task(
            self.hit_endpoint(caller, mode)
        )
        return response

    def perform_transaction(self, order_type, price):
        """
        Ask on the market for shares.
        {base_url}/venues/#{venue}/stocks/#{stock}/orders


        Different types of order:
            see `apimodels.VenueOrderBook`

        :param str type:
        :return dict:
        """
        result = self.book.send_order(
            self,
            order_type,
            price
        )

        print(result)
        return result


