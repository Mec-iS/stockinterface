# coding=utf-8
"""
An asynchronous client usimng Tornado-AsyncIO bridge:
<http://www.tornadoweb.org/en/stable/asyncio.html>

start Loop > run Coroutine > yield Future
"""
from secret import _KEY

from tornado.httpclient import HTTPRequest
import asyncio


def fetch(client, url, **kwargs):
    """
    Wrap the Tornado callback in a asyncio.Future
    <http://pepijndevos.nl/2014/07/09/mature-http-client-for-asyncio.html>
    :param client:
    :param url:
    :param kwargs:
    :return:
    """
    if 'data' in kwargs.keys() and kwargs['data']:
        request = HTTPRequest(
            url=url,
            method='POST',
            headers={
                        "X-Starfighter-Authorization": _KEY,
                        "accept-encoding": "gzip",
                        "content-type": "application/json"
                    },
            body=kwargs['data']
        )
    else:
        request = url
    fut = asyncio.Future()
    client.fetch(request, callback=fut.set_result)
    return fut




