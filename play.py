# coding=utf-8
"""
Levels playing module
"""
import asyncio
import json
from time import time

from async_client import fetch

__author__ = 'Lorenzo'


class Play:
    """
    General class for levels. Each subclass represents a level.

    """
    def __init__(self, agent):
        # Unique account assigned by level's instruction
        self.agent = agent
        # to be set pointing to the running loop when started
        # see self.start_play_loop()
        self.play_loop = None

        # players get a user account number at the beginning of each level
        from tornado.platform.asyncio import AsyncIOMainLoop

        # Tell Tornado to use the asyncio eventloop
        AsyncIOMainLoop().install()

        self.start_play_loop()

    def start_play_loop(self):

        # get the loop policy
        loop = asyncio.get_event_loop()
        loop.set_debug(True)

        # start the loop and inject coroutine
        loop.run_forever()

        setattr(self, 'play_loop', loop)

    def stop_play_loop(self):
        self.play_loop.stop()
        setattr(self, 'play_loop', None)

    @asyncio.coroutine
    def hit_endpoint(self, url, data=None, caller=None, attr=None):
        """
        Coroutine invoked to fetch the endpoint.

        :param object caller: the object requiring the data and in which the
                        response's body will be stored
        :param str url: url to be hit
        :param str attr: the attribute's name from the caller in which the
                        response's body will be stored
        :param dict data: POST data if needed
        :return dict: response's body
        """
        response = yield from fetch(
            url,
            data=data
        )
        read = response.body.decode()
        read = json.loads(read)
        print(read)
        if not read["ok"]:
            raise ValueError('play.hit_endpoint(). "ok" value is false,'
                             'there is an error in the response: ' + str(read["error"]))

        # set the attribute to store the result in the caller,
        # using different methods depending on attribute's type.
        # #todo: to be moved in a 'response receiving' method in the caller or
        # #todo: should emit an event to caller's listener
        if caller and attr:
            to_set = getattr(caller, attr)
            {
                'list': to_set.append(time(), read),
                'dict': setattr(caller, attr, read),
                'NoneType': setattr(caller, attr, read)
            }.get(
                type(getattr(caller, attr)).__name__
            )

    def dispatch(self, caller, url, attr, payload=None):
        """
        Collect the request and add the coroutine to the loop.

        :param object caller: the object requiring the data and in which the
                        response's body will be stored
        :param str url: url to be hit
        :param str attr: the attribute's name from the caller in which the
                        response's body will be stored
        :return: a Future
        """
        yield from self.play_loop.create_task(
            self.hit_endpoint(url, payload, caller, attr)
        )