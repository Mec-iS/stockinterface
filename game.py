# coding=utf-8
__author__ = 'Lorenzo'


class StockFighter:
    """
    General class for the game.

    <https://starfighter.readme.io/docs/getting-started>
    """
    pass


class Agent(StockFighter):
    """
    The agent for each account/venue pair. The player plays with a given
    account number for a given venue.
    """
    def __init__(self, account, venue):
        self.account = account    # the account number
        self.venue = venue        # the venue
        self.log = ()             # log of completed transactions

    def __str__(self):
        return "{__class__.__name__}: {account!r}, working in {venue!r}".format(
            __class__=self.__class__,
            account=self.account,
            venue=self.venue
        )

    def __repr__(self):
        return "{__class__.__name__}: {account!r}, working in {venue!r}".format(
            __class__=self.__class__,
            account=self.account,
            venue=self.venue
        )


class OrdersBook(StockFighter):
    """
    A statefull class to store the state of the stock market in a given level and
    in a given venue.

    Stockfighter Instructions:
        Stock exchanges give people placing orders limited control over the
        execution of those orders, in particular, under what circumstances the
        order "rests on" (goes into) the order book.

        The order book is the data structure that makes a stock exchange a stock
        exchange: it is two queues, ordered by priority, of all offers to buy a stock
        ("asks") and offers to sell a stock ("bid"). In Stockfighter, most exchanges
        implement price-time priority -- a "better" price
        always gets matched before a worse price, with ties getting broken by timestamp
        of the order.
    """
    def __init__(self):
        # set by Endpoint.VenueOrderBook
        self.listed = None
        self.orders = dict()
        # set by self.Order
        self.orders_sent = []

    def list_stocks(self):
        """List the stocks available for trading on a venue and store them in
    __class__.listed"""
        key = 'list_stocks'

        def _perform(self):
            self.url = self.modes[key]
            self.level.get(self, key)
            return self.listed

    def orders_by_stock(self):
        """List buy and sell offers in the order book for the given stock."""

        results = {}
        self.orders['stock'] = results


class Order(OrdersBook):
    """A stateless class for operations on the orders book."""
    params = ('stock', 'qty', 'direction', 'price', 'orderType',)

    def __init__(self, agent, **kwargs):
        """
        Construct a order to be sent.

        Example of order to be sent as payload to the endpoint:
            {
                "account": Agent.account
                "venue": Agent.venue,
                "stock": kwargs(stock),
                "price": kwargs(price),
                "qty": kwargs(qty),
                "direction": kwargs(direction),
                "orderType": kwargs(order_type)
            }

        :param Agent agent:
        :param kwargs: a dictionary with keys as expressed in `self.params`
        :return:
        """
        super().__init__()
        self.agent = agent
        self.account = agent.account
        self.venue = agent.venue
        if all(kwargs.get(k) for k in self.params):
            self.final_order = kwargs
        else:
            raise ValueError('Dispatch._build_data():'
                             'Missing needed argument: %s.' % (self.params, ))

    def __str__(self):
        return "{__class__.__name__}: {id!r} created by {agent!r}".format(
            __class__=self.__class__,
            agent=self.agent,
            id=id(self)
        )

    def __repr__(self):
        return "{__class__.__name__}: {id!r} created by {agent!r}".format(
            __class__=self.__class__,
            agent=self.agent,
            id=id(self)
        )

    def _build_data(self):
        """Build request's data to perform a ask/bid action."""
        import json

        post_data = {
            "account": self.account,
            "venue": self.venue
        }
        post_data.update(self.final_order)

        return json.dumps(post_data)

    def place_order(self):
        """Build and send an order via the async loop. Create an Endpoint instance,
        """
        import time
        print(repr(self) + " is passed to Dispatcher")
        self.orders_sent.append((time.time(), self))
        pass

