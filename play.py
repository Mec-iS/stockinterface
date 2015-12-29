# coding=utf-8
"""
A module is for I/O with the Web.
"""
import json
from time import time
import concurrent.futures

from client import _request, _response

__author__ = 'Lorenzo'


class Play:
    """
    A stateless class for dispatching requests.
    """
    def __init__(self):
        # to be set pointing to the running loop when started
        # see self.start_play_loop()
        self.play = 'on'

    @classmethod
    def hit_endpoint(cls, url, caller=None, attr=None):
        """
        Fetch a single url for a resource.

        :param Request url: request to the url to be hit
        :param object caller: the object requiring the data and in which the
               response's body will be stored
        :param str attr: the attribute's name from the caller in which the
               response's body will be stored
        :return dict: response's body
        """
        # fetch using `client`
        try:
            body, _ = _response(_request(url))
        except ConnectionError as e:
            raise e
        except ValueError as e:
            raise e

        read = json.loads(body)
        print(read)

        cls.store_response(caller, attr, read)

        return read

    @classmethod
    def run_async_executor(cls, queue, caller, attr):
        """
        Run multiple _response functions in a queue using a ThreadPoolExecutor.

        :param list queue: a list of Request(s)
        :return: bool
        """
        from urllib.request import Request
        assert isinstance(queue, list)
        assert all(isinstance(q, Request) for q in queue)

        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            # Start the load operations and mark each future with its URL
            future_to_url = {
                executor.submit(_response(req)): req.get_full_url()
                for req in queue
            }
            for future in concurrent.futures.as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    data = future.result()
                    read = json.loads(data)
                    cls.store_response(caller, attr, read)
                except Exception as exc:
                    print('%r generated an exception: %s' % (url, exc))
                    return False
                else:
                    print('%r page is %d bytes' % (url, len(data)))
                    return False

        return True

    @classmethod
    def dispatch(cls, caller, url, attr=None):
        """
        Collect the request and add the coroutine to the loop.

        :param object caller: the object requiring the data and in which the
                        response's body will be stored
        :param Request url: Request to be fulfilled or a list of Request(s)
        :param str attr: the attribute's name from the caller in which the
                        response's body will be stored
        """
        return {
            'list': cls.run_async_executor(url, caller, attr),
            'str': cls.hit_endpoint(url, caller, attr)
        }.get(str(type(url)))

    @classmethod
    def store_response(cls, body, caller, attr):
        # set the attribute to store the result in the caller,
        # using different methods depending on attribute's type.
        # #todo: to be moved in a 'response receiving' method in the caller or
        # #todo: should emit an event to caller's listener
        if caller and attr:
            {
                'list': getattr(caller, attr).append(time(), body),
                'dict': setattr(caller, attr, body),
                'NoneType': setattr(caller, attr, body)
            }.get(
                type(getattr(caller, attr)).__name__
            )