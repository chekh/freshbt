from enum import Enum
from dataclasses import dataclass
from datetime import datetime

class OrderType(Enum):
    BUY = "buy"
    SELL = "sell"
    CLOSE = "close"
    LIMIT = "limit"
    STOP = "stop"
    OCO = "oco"

class TransactionType(Enum):
    ORDER_ADD = "order_add"
    ORDER_UPDATE = "order_update"
    ORDER_DELETE = "order_delete"
    DEAL_ADD = "deal_add"

@dataclass
class Order:
    order_type: OrderType
    symbol: str
    volume: float
    price: float
    time_placed: datetime
    delay: int
    stop_loss: float
    take_profit: float
    action: OrderType
    transaction_type: TransactionType
    linked_order: 'Order' = None  # Ссылка на связанный ордер для OCO

    def is_expired(self, current_time):
        return self.time_placed + self.delay < current_time

    def execute(self, current_time):
        self.time_executed = current_time

    def cancel(self, current_time):
        self.time_cancelled = current_time
