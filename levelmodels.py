# coding=utf-8
"""
Levels playing module
"""
from apimodels import StockFighter

__author__ = 'Lorenzo'


class Level(StockFighter):
    """
    General class for levels. Each subclass represtns a level.

    """
    def __init__(self, account):
        # players get a user account number at the beginning of each level
        self.account = account
