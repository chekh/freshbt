class OrderBook:
    def __init__(self):
        self.orders = []

    def add_order(self, order):
        self.orders.append(order)

    def remove_order(self, order):
        self.orders = [o for o in self.orders if o != order]

    def get_pending_orders(self, current_time):
        return [order for order in self.orders if order.time_placed + order.delay <= current_time]
