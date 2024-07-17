from utils.statistics import BacktestStatistics
from utils.metrics import Metrics
from broker.enums import OrderType, DealType, EntryType, TransactionType
from data.interfaces import IDataHandler
from strategies.interfaces import IStrategy
from broker.interfaces import IBroker
from utils.interfaces import ILogger

class Backtester:
    def __init__(self, data_handler: IDataHandler, strategy: IStrategy, broker: IBroker, logger: ILogger):
        self.data_handler = data_handler
        self.strategy = strategy
        self.broker = broker
        self.logger = logger
        self.statistics = BacktestStatistics()
        self.metrics = Metrics(self.statistics)

    def run(self):
        while self.data_handler.has_more_data():
            current_bar = self.data_handler.get_next_bar()
            self.broker.current_time += 1  # Увеличиваем текущий счетчик времени

            # Обновление эквити и маржи
            current_prices = {position.symbol: current_bar.Close for position in self.broker.get_open_positions()}
            self.broker.calculate_equity(current_prices)
            self.broker.calculate_margin(current_prices)

            # Проверка условий стоп-лосса и тейк-профита
            open_positions = self.broker.get_open_positions()
            for position in open_positions:
                close_order = self.check_stop_loss_and_take_profit(position, current_bar, self.data_handler.get_lower_timeframe_bars(current_bar))
                if close_order:
                    self.broker.execute_order(close_order, current_bar)
                    self.broker.update_balance_and_portfolio()
                    self.statistics.update(self.broker.deals[-1])  # Обновление статистики

            # Исполнение отложенных ордеров
            pending_orders = self.broker.get_pending_orders()
            for order in pending_orders:
                if self.order_conditions_met(order, current_bar):
                    self.broker.execute_order(order, current_bar)
                    self.broker.update_balance_and_portfolio()
                    self.statistics.update(self.broker.deals[-1])  # Обновление статистики

            # Обновление стратегии
            self.strategy.update(current_bar)

            # Исполнение новых ордеров
            new_orders = self.strategy.generate_orders()
            for order in new_orders:
                if self.broker.check_funds(order):
                    self.broker.place_order(order)  # Размещение нового ордера с учетом задержки
                    self.broker.execute_order(order, current_bar)
                    self.broker.update_balance_and_portfolio()
                    self.statistics.update(self.broker.deals[-1])  # Обновление статистики

            # Запись результатов
            self.logger.log_results(self.broker, current_bar)

            # Переход к следующему бару
            self.data_handler.move_to_next_bar()

        # Завершение
        self.finalize_results(self.broker)
        self.statistics.print_statistics()  # Печать итоговой статистики
        self.metrics.calculate_metrics()  # Расчет метрик
        self.metrics.print_metrics()  # Печать метрик

    def check_stop_loss_and_take_profit(self, position, current_bar, lower_timeframe_bars):
        # Проверка условий стоп-лосса и тейк-профита
        if position.position_type == DealType.BUY:
            if current_bar.Low <= position.stop_loss:
                return self.generate_close_order(position, position.stop_loss)
            if current_bar.High >= position.take_profit:
                return self.generate_close_order(position, position.take_profit)
        elif position.position_type == DealType.SELL:
            if current_bar.High >= position.stop_loss:
                return self.generate_close_order(position, position.stop_loss)
            if current_bar.Low <= position.take_profit:
                return self.generate_close_order(position, position.take_profit)
        return None

    def generate_close_order(self, position, price):
        return Order(
            order_type=OrderType.CLOSE,
            symbol=position.symbol,
            volume=position.volume,
            price=price,
            time_placed=self.broker.get_current_time(),
            delay=0,
            stop_loss=None,
            take_profit=None,
            action=OrderType.CLOSE,
            transaction_type=TransactionType.ORDER_UPDATE
        )

    def order_conditions_met(self, order, current_bar):
        # Проверка выполнения условий для отложенного ордера
        return True  # Упростим проверку для примера

    def finalize_results(self, broker):
        # Завершение и сохранение итоговых результатов
        pass
