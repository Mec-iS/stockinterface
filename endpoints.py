# coding=utf-8
"""
General model and endpoints models
"""
from game import StockFighter
__author__ = 'Lorenzo'


class Endpoint(StockFighter):
    """
    General class for endpoints. Each subclass represents
    a specific method for each endpoint.
    """
    def __init__(self):
        # URL on which the different endpoints are based
        self.base_url = "https://api.stockfighter.io/ob/api/"
        # The url actually in use (some endpoints may have different 'modes')
        self.url = None

        self.response = None
        self.heartbeat = None

    def __str__(self):
        return "Endpoint {__class__.__name__}: {url!r} ready to be fetched, response={response!r}".format(
            __class__=self.__class__,
            url=self.url,
            response=bool(self.response is not None)
        )

    def __repr__(self):
        return "Endpoint {__class__.__name__}: {url!r}, id={id!r}, hash={hash!r}".format(
            __class__=self.__class__,
            url=self.url,
            id=id(self),
            hash=hash(self)
        )

    def _root(self):
        return self.base_url


class APIHeartBeat(Endpoint):
    """
    Endpoint: Check The API Is Up
    A simple health check for the API

    Method: GET
    """

    def __init__(self):
        super().__init__()
        self.url = self.base_url + "heartbeat"


class VenueHeartBeat(Endpoint):
    """
    Endpoint: Check A Venue Is Up.

    Method: GET

    Documentation:
        A modestly less simple health check for the API.
        Check if a venue is up (usually venues are created at initialization
        of each level)
    """
    def __init__(self, venue):
        super().__init__()
        self.url = self.base_url + "venues/{}/heartbeat".format(venue)


class Stocks(Endpoint):
    """
    Endpoint:
        * list stocks: "venues/TESTEX/stocks/"
          GET: [{ "name": "ABC Co", "symbol": "ABC" },
               { "name": "DFE Inc", "symbol": "DFE" }, ...]
        * list offers for a stock and buy/sell stocks: "venues/TESTEX/stocks/FOOBAR"
          GET: {"ok": true, "venue": "BBBBEX",
                "symbol": "ORI","ts": "2015-12-23T13:53:51.517565036Z",
                "bids": [
                    {
                        "price": 3231,
                        "qty": 1777,
                        "isBuy": true
                    },
                    {
                        "price": 3215,
                        "qty": 1777,
                        "isBuy": true
                    },
                    {
                        "price": 3199,
                        "qty": 1777,
                        "isBuy": true
                    }
                ],
                "asks": [
                    {
                        "price": 3478,
                        "qty": 222,
                        "isBuy": false
                    },
                    {
                        "price": 3495,
                        "qty": 222,
                        "isBuy": false
                    },
                    {
                        "price": 3512,
                        "qty": 222,
                        "isBuy": false
                    }
                ]
              }
          * place an order (ask/bid)
            POST: {
                      "ok": true,
                      "symbol": "FAC",
                      "venue": "OGEX",
                      "direction": "buy",
                      "originalQty": 100,
                      "qty": 20,   // this is the quantity *left outstanding*
                      "price":  5100, // the price on the order -- may not match that of fills!
                      "type": "limit",
                      "id": 12345, // guaranteed unique *on this venue*
                      "account" : "OGB12345",
                      "ts": "2015-07-05T22:16:18+00:00", // ISO-8601 timestamp for when we received order
                      "fills":
                        [
                          {
                            "price": 5050,
                            "qty": 50
                            "ts": "2015-07-05T22:16:18+00:00"
                          }, ... // may have zero or multiple fills.  Note this order presumably has a total of 80 shares worth
                        ],
                      "totalFilled": 80,
                      "open": true
                    }
          * Get a quick look at the most recent trade information for a stock
            GET: {
                    "ok": true,
                    "symbol": "FAC",
                    "venue": "OGEX",
                    "bid": 5100, // best price currently bid for the stock
                    "ask": 5125, // best price currently offered for the stock
                    "bidSize": 392, // aggregate size of all orders at the best bid
                    "askSize": 711, // aggregate size of all orders at the best ask
                    "bidDepth": 2748, // aggregate size of *all bids*
                    "askDepth": 2237, // aggregate size of *all asks*
                    "last": 5125, // price of last trade
                    "lastSize": 52, // quantity of last trade
                    "lastTrade": "2015-07-13T05:38:17.33640392Z", // timestamp of last trade
                    "quoteTime": "2015-07-13T05:38:17.33640392Z" // ts we last updated quote at (server-side)
                }

    Accepted parametersfor POST:
        account: String EXB123456
        venue: String TESTEX
        stock: String FOOBAR
        price: Integer Desired price (an integer: $53.42 becomes 5342)
        qty: Integer Desired quantity
        direction: String Whether you want to "buy" or "sell"
        orderType: String The order type

    Order types:
        * Limit orders: (in API, "limit"): The most common order type, which works
        as specified above.
        * Market orders: (in API, "market"): An order type you should never use for
        any reason, most especially not because you're a retail trader or an evil level
        designer suggested you try it. A market order doesn't specify a price -- it
        just continues matching orders until it is filled or it has exhausted one side
        of the order book. It never rests on the order book. Market orders routinely blow
        up in the face of people placing them, because what happens when you do a market
        order for 10 shares against a book which has 9 @ $10 and 1 @ $12,000? Yep, you pay $12,090.
        * Fill-or-Kill orders_ (in API, "fill-or-kill"): Fill-or-kill (FOK) orders let you
        specify a limit price, like a limit order, but never rest on the book. Also, they're
        all-or-nothing (AON, in Wall Street parlance). Normally, if you place an order for 10
        shares and the market can only give you 8, you get 8. With a FOK order, you get 0
        (and the order gets immediately canceled).
        * Immediate-or-cancel orders: (in API, "immediate-or-cancel"): Like FOK in that the order
        executes instantly and never rests on the book, but it isn't all-or-nothing. If you can
        only get 8 shares out of the 10 you wanted, you'll get the 8 shares.


    """
    def __init__(self, venue, stock):
        super().__init__()

        self.venue = venue
        self.stock = stock

        self.actions = (
            ('list_stocks', 'GET', self.base_url + 'venues/{}/stocks/'.format(self.venue), ),
            ('orders_by_stock', 'GET', self.base_url + 'venues/{}/stocks/{}'.format(self.venue, self.stock), ),
            ('submit_order', 'POST', self.base_url + 'venues/{}/stocks/{}/orders'.format(self.venue, self.stock), ),
            ('get_quote', 'GET', self.base_url + 'venues/{}/stocks/{}/quote'.format(self.venue, self.stock), ),
        )

        # a mini-factory for attributes getting the different urls
        # each attribute returns the right endpoint url from the dictionary above
        for v in self.actions:
            setattr(self, v[0], v[2])

    def __str__(self):
        return ('Endpoint {__class__.__name__}: object ready, choose a URL using the right attribute:\n'
                '\t\t\t\t {actions!r}, response={response!r}').format(
            __class__=self.__class__,
            actions=tuple((a[0], a[1]) for a in self.actions),
            response=bool(self.response is not None)
        )

    def __repr__(self):
        return "Endpoint {__class__.__name__}: id={id!r}, hash={hash!r}".format(
            __class__=self.__class__,
            id=id(self),
            hash=hash(self)
        )


class Orders(Endpoint):
    """
    Endpoint:
      * Status For An Existing Order
        GET: {
              "ok": true,
              "symbol": "ROBO",
              "venue": "ROBUST",
              "direction": "buy",
              "originalQty": 85,
              "qty": 40,
              "price": 993,
              "orderType": "immediate-or-cancel",
              "id": 1,
              "account": "FOO123",
              "ts": "2015-08-10T16:10:32.987288+09:00",
              "fills": [
                {
                  "price": 366,
                  "qty": 45,
                  "ts": "2015-08-10T16:10:32.987292+09:00"
                }
              ],
              "totalFilled": 85,
              "open": true
            }
      * Cancel An Order
        GET: {
              "ok": true,
              "symbol": "ROBO",
              "venue": "ROBUST",
              "direction": "buy",
              "originalQty": 85,
              "qty": 0,  // note that qty will always be 0 for canceled orders
              "price": 993,
              "orderType": "immediate-or-cancel",
              "id": 1,
              "account": "FOO123",
              "ts": "2015-08-10T16:10:32.987288+09:00",
              "fills": [
                {
                  "price": 366,
                  "qty": 45,
                  "ts": "2015-08-10T16:10:32.987292+09:00"
                }
              ],
              "totalFilled": 85,
              "open": false
            }
    """
    def __init__(self, venue, stock, order_id):
        super().__init__()
        self.venue = venue
        self.stock = stock
        self.order_id = order_id  # unique at venue level

        self.actions = {
            'order_status': ('GET', self.base_url + 'venues/{venue}/stocks/{stock}/orders/{id}'.format(
                venue=self.venue,
                stock=self.stock,
                id=self.order_id),
            ),
            'cancel_order': ('POST', self.base_url + 'venues/{venue}/stocks/{stock}/orders/{id}/cancel'.format(
                venue=self.venue,
                stock=self.stock,
                id=self.order_id),
            ),
        }

        # a mini-factory for the different methods
        # each method returns the right endpoint url form the dictionary above
        for k, v in self.actions.items():
            setattr(self, k, lambda x: str(k[1]))


class Account(Endpoint):
    """
    Endpoint:
      * Status For All Orders
        GET: {
              "ok": true,
              "venue": "ROBUST",
              "orders": [
                {
                  "symbol": "ROBO",
                  "venue": "ROBUST",
                  "direction": "buy",
                  "originalQty": 85,
                  "qty": 40,
                  "price": 993,
                  "orderType": "immediate-or-cancel",
                  "id": 1,
                  "account": "FOO123",
                  "ts": "2015-08-10T16:10:32.987288+09:00",
                  "fills": [
                    {
                      "price": 366,
                      "qty": 45,
                      "ts": "2015-08-10T16:10:32.987292+09:00"
                    }
                  ],
                  "totalFilled": 85,
                  "open": true
                },
                ... // We'll show any number of orders.
              ]
            }
      * Status For All Orders In A Stock
        GET: {
              "ok": true,
              "venue": "ROBUST",
              orders: [
                {
                  "symbol": "ROBO",
                  "venue": "ROBUST",
                  "direction": "buy",
                  "originalQty": 85,
                  "qty": 40,
                  "price": 993,
                  "orderType": "immediate-or-cancel",
                  "id": 1,
                  "account": "FOO123",
                  "ts": "2015-08-10T16:10:32.987288+09:00",
                  "fills": [
                    {
                      "price": 366,
                      "qty": 45,
                      "ts": "2015-08-10T16:10:32.987292+09:00"
                    }
                  ],
                  "totalFilled": 85,
                  "open": true
                },
                ... // We'll show any number of orders.
              ]
            }
    """
    def __init__(self, venue, account, stock=None):
        super().__init__()
        self.venue = venue
        self.account = account
        self.stock = stock

        self.actions = {
            'list_all_orders': (),
            'list_orders_by_stock': ()
        }