from .interfaces import IBroker
from .order_book import OrderBook
from .position_book import PositionBook
from utils.commission import Commission

class Broker(IBroker):
    def __init__(self, initial_balance, margin_requirement=0.01, leverage=1, enable_margin_call=True, commission_calculator=None):
        self.balance = initial_balance
        self.equity = initial_balance
        self.margin = 0.0
        self.free_margin = initial_balance
        self.margin_level = 0.0
        self.order_book = OrderBook()
        self.position_book = PositionBook()
        self.deals = []  # Список сделок
        self.current_time = 0  # Счетчик текущего времени в барах
        self.margin_requirement = margin_requirement
        self.leverage = leverage
        self.enable_margin_call = enable_margin_call  # Опция для проверки маржин-колла
        self.commission_calculator = commission_calculator or Commission()  # Используем внедрение зависимости

    def get_open_positions(self):
        return self.position_book.get_open_positions()

    def get_pending_orders(self):
        return self.order_book.get_pending_orders(self.current_time)

    def place_order(self, order):
        order.transaction_type = TransactionType.ORDER_ADD
        self.order_book.add_order(order)

    def execute_order(self, order, current_bar):
        raise NotImplementedError("This method should be implemented by subclasses")

    def update_balance_and_portfolio(self):
        # Обновление баланса и состояния портфеля
        self.update_balance()
        self.update_portfolio()
        if self.enable_margin_call:
            self.check_margin_call()

    def update_balance(self):
        # Обновление баланса
        self.balance = sum(deal.profit for deal in self.deals)

    def update_portfolio(self):
        # Обновление эквити и маржи
        current_prices = {position.symbol: position.current_price for position in self.position_book.get_open_positions()}
        self.calculate_equity(current_prices)
        self.calculate_margin(current_prices)

    def check_margin_call(self):
        # Проверка маржин-колла
        if self.margin > 0 and self.margin_level < 100:
            print("Margin call! Equity is less than margin.")
            # Здесь можно реализовать логику закрытия позиций или другие действия

    def check_funds(self, order):
        # Проверка наличия достаточных средств для исполнения ордера
        required_margin = order.volume * order.price * self.margin_requirement / self.leverage
        return self.free_margin >= required_margin

    def calculate_equity(self, current_prices):
        unrealized_pnl = 0.0
        for position in self.position_book.get_open_positions():
            if position.position_type == OrderType.BUY:
                unrealized_pnl += (current_prices[position.symbol] - position.entry_price) * position.volume
            elif position.position_type == OrderType.SELL:
                unrealized_pnl += (position.entry_price - current_prices[position.symbol]) * position.volume
        self.equity = self.balance + unrealized_pnl
        return self.equity

    def calculate_margin(self, current_prices):
        margin = 0.0
        for position in self.position_book.get_open_positions():
            margin += position.volume * current_prices[position.symbol] * self.margin_requirement / self.leverage
        self.margin = margin
        self.free_margin = self.equity - self.margin
        self.margin_level = (self.equity / self.margin) * 100 if self.margin > 0 else 0.0
        return self.margin, self.free_margin, self.margin_level

    def get_current_time(self):
        return self.current_time

    def calculate_leverage(self, order_volume, order_price):
        # Расчет необходимой маржи с учетом кредитного плеча
        return order_volume * order_price / self.leverage
