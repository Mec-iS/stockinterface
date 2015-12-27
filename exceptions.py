# coding=utf-8
"""
Exceptions' model
"""

__author__ = 'Lorenzo'


class APIisDown(Exception):
    pass


class ConnectionFault(Exception):
    """
    Generic problem opening the url or in the response.
    """
    pass
