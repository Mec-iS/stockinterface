# coding=utf-8
"""
An asynchronous client usimng Tornado-AsyncIO bridge:
<http://www.tornadoweb.org/en/stable/asyncio.html>

start Loop > run Coroutine > yield Future
"""
from secret import _KEY

from tornado.httpclient import HTTPRequest
import asyncio

# create Tornado HTTP Async client
from tornado.httpclient import AsyncHTTPClient
http_client = AsyncHTTPClient()


def fetch(url, data=None):
    """
    Wrap the Tornado callback in a asyncio.Future
    <http://pepijndevos.nl/2014/07/09/mature-http-client-for-asyncio.html>
    :param url:
    :param JSON data:
    :return: a Future()
    """
    if data:
        # a POST needs a Request object
        assert data
        request = HTTPRequest(
            url=url,
            method='POST',
            headers={
                        "X-Starfighter-Authorization": _KEY,
                        "accept-encoding": "gzip",
                        "content-type": "application/json"
                    },
            body=data
        )
    else:
        # a GET needs just a url
        request = url
    fut = asyncio.Future()
    http_client.fetch(request, callback=fut.set_result)
    return fut




