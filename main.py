# coding=utf-8
__author__ = 'Lorenzo'

# ############################### Algorithm ################################ #

account = "TST00000001"
# Venue: EVTY Oak Park Exchange
venue = "TSTEX"
# Action:
action = "buy"  # bid or ask, use "buy" or "sell"
# Quantity:
q = 100000  # shares
# Company: BrainIdea Corp.
company = "TEST"

from game import Agent, OrdersBook, Order

# create an agent with credentials for a venue
agent = Agent(account, venue)
# create a orders book to manage the quoting
book = OrdersBook(
    agent=agent
)

"""
Example of order to be sent as payload to the endpoint:
    {
        "account": Agent.account        # account number
        "venue": Agent.venue,           # venue
        "stock": kwargs(stock),         # name of stock
        "price": kwargs(price),         # price
        "qty": kwargs(qty),             # quantity
        "direction": kwargs(direction), # buy or sell
        "orderType": kwargs(order_type) # order type
    }
"""

# initialize the order
order = Order(orders_book=book)

# define a price by using the venue's stocks data
current_orders = order.orders_by_stock()
prices = tuple(a['price'] for a in current_orders)
# define a price using some simple math
price = (max(prices) + max(prices)/100 * 5)

# set your order and your price
order_data = dict(
    venue=venue,
    direction=action,
    qty=1000,
    stock=company
)
order_data["price"] = price

# fill order payload
order.cook_order(**order_data)
# dispatch the order
result = book.place_order(order)  # result can be 'shipped', 'queued' or 'rejected'

# update the OrderBook()
current_orders = order.orders_by_stock()

# stop the loop
book.play_loop.stop_play_loop()