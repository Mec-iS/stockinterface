# coding=utf-8
__author__ = 'Lorenzo'

# ############################### Algorithm ################################ #

# Create an Agent(account, venue)
# Loop = Play(Agent) > start the loop
# Create a OrderBook() to follow the instant state of the venue
# Create a Order(Agent, Loop, order_data)
# perform Order
# Stop loop

# ################################ Level 1 ################################# #
account = "YCH86804436"
# Venue: EVTY Oak Park Exchange
venue = "CDKEX"
# Action:
action = "buy"
# Quantity:
q = 100000  # shares
# Company: BrainIdea Corp.
company = "IFZI"

from levelmodels import Level, Action

level = Level(account)
level.start_level_loop()

qty = 0
while qty < q+1:
    ask1 = Action(
        account,
        venue=venue,
        direction=action,
        qty=1000,
        stock=company
    )

    prices = tuple(a['price'] for a in ask1.book.get_asks_and_bids())
    import time
    time.sleep(0.5)

    price = (max(prices) + max(prices)/100 * 5)
    print(price)
    time.sleep(1)

    ask1.perform_transaction('limit', price)

level.stop_level_loop()