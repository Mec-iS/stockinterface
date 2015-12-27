# coding=utf-8
"""
Levels playing module
"""
import asyncio
import json
from endpoints import StockFighter
from async_client import fetch

__author__ = 'Lorenzo'


class Play(StockFighter):
    """
    General class for levels. Each subclass represents a level.

    """
    def __init__(self, agent):
        # Unique account assigned by level's instruction
        self.agent = agent
        # to be set when loop starts
        self.play_loop = None

        # players get a user account number at the beginning of each level
        from tornado.platform.asyncio import AsyncIOMainLoop

        # Tell Tornado to use the asyncio eventloop
        AsyncIOMainLoop().install()

        self.http_client = None

    def start_play_loop(self):
        from tornado.httpclient import AsyncHTTPClient

        # get the loop policy
        loop = asyncio.get_event_loop()
        loop.set_debug(True)

        # create Tornado HTTP Async client
        self.http_client = AsyncHTTPClient()

        # start the loop and inject coroutine
        loop.run_forever()

        setattr(self, 'play_loop', loop)

    def stop_play_loop(self):
        self.play_loop.stop()
        setattr(self, 'play_loop', None)

    @asyncio.coroutine
    def hit_endpoint(self, caller, mode):
        """
        Coroutine to fetch the endpopint
        :param apimodels.Endpoint:
        :param tornado.httpclient.AsyncHTTPClient http_client:
        :return None: set `response` attribute in the calling class
        """
        print('fetching heartbeat')

        response = yield from fetch(
            self.http_client,
            caller.url
        )
        read = response.body.decode()
        read = json.loads(read)
        print(read)
        if not read["ok"]:
            raise ValueError('play.hit_endpoint(). "ok" value is false,'
                             'there is an error in the payload: ' + str(read["error"]))
        # storing the response body in the class object
        return setattr(
            caller,
            mode,
            read)

    def get(self, caller, mode):
        """

        :param Endpoint caller:
        :param str mode:
        :return:
        """
        response = yield from self.play_loop.create_task(
            self.hit_endpoint(caller, mode)
        )
        return response