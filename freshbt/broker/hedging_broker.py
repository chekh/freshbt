from .broker import Broker
from .order import Order, OrderType, TransactionType
from .position import Position
from .deal import Deal
from .enums import DealType, EntryType

class HedgingBroker(Broker):
    def execute_order(self, order, current_bar):
        commission_cost = self.commission_calculator.calculate(order.volume, order.price)
        if order.order_type == OrderType.CLOSE:
            position = self.position_book.find_position(order.symbol)
            if position:
                position.close(order.price, self.current_time)
                self.position_book.remove_position(position)
                profit = position.get_profit() - commission_cost  # Учитываем комиссию
                deal = Deal(
                    order_id=order.ticket,
                    time=self.current_time,
                    deal_type=DealType.SELL if position.position_type == OrderType.BUY else DealType.BUY,
                    entry_type=EntryType.CLOSE,
                    symbol=order.symbol,
                    volume=order.volume,
                    price=order.price,
                    commission=commission_cost,
                    swap=position.swap,
                    profit=profit,
                    magic_number=order.magic_number,
                    comment=order.comment,
                    transaction_type=TransactionType.DEAL_ADD
                )
                self.deals.append(deal)
                self.balance += profit  # Обновление баланса на основе прибыли/убытка
                if order.linked_order:
                    self.order_book.remove_order(order.linked_order)  # Отменяем связанный ордер в случае OCO
        else:
            new_position = Position(
                symbol=order.symbol,
                volume=order.volume,
                entry_price=order.price,
                open_time=self.current_time,
                position_type=OrderType.BUY if order.volume > 0 else OrderType.SELL,
                stop_loss=order.stop_loss,
                take_profit=order.take_profit,
                magic_number=order.magic_number,
                comment=order.comment
            )
            self.position_book.add_position(new_position)
            deal = Deal(
                order_id=order.ticket,
                time=self.current_time,
                deal_type=DealType.BUY if new_position.position_type == OrderType.BUY else DealType.SELL,
                entry_type=EntryType.OPEN,
                symbol=order.symbol,
                volume=order.volume,
                price=order.price,
                commission=commission_cost,
                magic_number=order.magic_number,
                comment=order.comment,
                transaction_type=TransactionType.DEAL_ADD
            )
            self.deals.append(deal)
            if order.linked_order:
                self.order_book.remove_order(order.linked_order)  # Отменяем связанный ордер в случае OCO
        self.update_balance_and_portfolio()
