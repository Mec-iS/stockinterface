# coding=utf-8
"""
General model and endpoints models
"""
import urllib.response
import urllib.request
import urllib.parse
import json

from secret import _KEY
from exceptions import APIisDown

__author__ = 'Lorenzo'


class StockFighter:
    """
    General class for the game.

    <https://starfighter.readme.io/docs/getting-started>
    """
    pass


class Endpoint(StockFighter):
    """
    General class for endpoints. Each subclass represents
    an endpoint.
    """
    base_url = "https://api.stockfighter.io/ob/api/"

    def get_base_url(self):
        return self.base_url


class HeartBeat(Endpoint):
    """
    Endpoint: Check if the API is up.
    """
    url = "https://api.stockfighter.io/ob/api/heartbeat"

    @classmethod
    def check_if_api_is_up(cls):
        req = urllib.request.Request(cls.url)
        with urllib.request.urlopen(req) as response:
            read = json.loads(
                response.read().decode('utf-8')
            )
        if not read['ok']:
            raise APIisDown('API is down. No HeartBeat')
        return read
