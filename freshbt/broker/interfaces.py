from abc import ABC, abstractmethod

class IBroker(ABC):
    @abstractmethod
    def get_open_positions(self):
        pass

    @abstractmethod
    def get_pending_orders(self):
        pass

    @abstractmethod
    def place_order(self, order):
        pass

    @abstractmethod
    def execute_order(self, order, current_bar):
        pass

    @abstractmethod
    def update_balance_and_portfolio(self):
        pass

    @abstractmethod
    def check_funds(self, order):
        pass

    @abstractmethod
    def calculate_equity(self, current_prices):
        pass

    @abstractmethod
    def calculate_margin(self, current_prices):
        pass

    @abstractmethod
    def get_current_time(self):
        pass

    @abstractmethod
    def calculate_leverage(self, order_volume, order_price):
        pass
