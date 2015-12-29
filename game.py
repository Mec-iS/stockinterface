# coding=utf-8

from play import Play
from endpoints import VenueList, Stocks

__author__ = 'Lorenzo'


class Agent:
    """
    The agent for each account/venue pair. The player plays with a given
    account number for a given venue.
    """
    __slots__ = ('account', 'venue', 'log', )

    def __init__(self, account, venue):
        self.account = account    # the account number
        self.venue = venue        # the venue
        self.log = []             # log of completed transactions

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


class OrdersBook:
    """
    A statefull class to store the state of the stock market in a given level and
    in a given venue.

    Stockfighter Instructions:
        Stock exchanges give people placing orders limited control over the
        execution of those orders, in particular, under what circumstances the
        order "rests on" (goes into) the order book.

        The order book is the data structure that makes a stock exchange a stock
        exchange: it is two queues, ordered by priority, of all offers to buy a stock
        ("bid") and offers to sell a stock ("ask"). In Stockfighter, most exchanges
        implement price-time priority -- a "better" price
        always gets matched before a worse price, with ties getting broken by timestamp
        of the order.

    In this interface we use the OrdersBook class to place orders and keep track of
    the state of the market.
    """
    def __init__(self, agent):

        # set basic attributes for the (venue, agent) operations
        self.agent = agent
        self.account = agent.account
        self.venue = agent.venue

        # general venue's info
        self.listed = None          # response from VenueList.url
        self.orders = []            # response from Stocks.orders_by_stock

        # set by self.Order
        self.orders_queued = []    # orders processing
        self.orders_sent = []       # orders sent
        self.orders_completed = []   # orders accepted
        self.orders_failed = []     # orders failed

        # load the stocks list
        #self.list_stocks()

    def list_stocks(self):
        """List the stocks available for trading on a venue and store them in
        `self.listed`"""
        # find the right endpoint URL
        endpoint = VenueList(
            venue=self.venue
        ).url

        # send to dispatcher
        Play().dispatch(
            caller=self,
            url=endpoint,
            attr='listed')

    def _build_order_data(self, order):
        """Build request's data to perform a ask/bid action, data is taken from
        the Order's constructor."""
        import json

        post_data = {
            "account": self.account,
            "venue": self.venue
        }
        post_data.update(order.order_payload)

        return json.dumps(post_data)

    def place_order(self, order):
        """Build and send an order via the async loop. Create an Endpoint instance,
        """
        print(repr(self) + " is passed to Dispatcher")
        # find the right endpoint URL
        endpoint = Stocks(
            stock=order.order_payload['stock'],
            venue=order.order_payload['venue']
        ).submit_order
        # send to dispatcher
        self.play_loop.dispatch(
            caller=self,
            url=endpoint,
            attr=None,
            payload=self._build_order_data(order)
        )

        # add order to sent orders in the orders books
        setattr(self, 'orders_sent', order)


class Order:
    """A stateless class representing a single order, a single action/event
    playable by an agent."""
    params = ('stock', 'qty', 'direction', 'price', 'orderType',)

    def __init__(self, orders_book):
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

        :param OrdersBook orders_book:
        :return: Order instance
        """
        assert isinstance(orders_book, OrdersBook)

        self.orders_book = orders_book
        self.agent = orders_book.agent
        self.venue = orders_book.venue
        self.account = orders_book.account

        # to be set when the order is 'cooked'
        self.order_payload = None

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

    def orders_by_stock(self):
        """List buy and sell offers in the order book for the given stock."""
        # find the right endpoint URL
        endpoint = Stocks(
            venue=self.venue,
            stock=self.order_payload["stock"]
        ).orders_by_stock

        # send to dispatcher
        Play().dispatch(
            caller=self.orders_book,     # we want to store this data in orders book
            url=endpoint,
            attr='orders')

    def cook_order(self, **kwargs):
        assert all(kwargs.get(k) for k in self.params)
        setattr(self, 'order_payload', kwargs)




