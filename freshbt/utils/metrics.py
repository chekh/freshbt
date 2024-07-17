import math

class Metrics:
    def __init__(self, statistics):
        self.statistics = statistics
        self.metrics = {}

    def calculate_metrics(self):
        self.metrics["profit_factor"] = self.profit_factor()
        self.metrics["sharpe_ratio"] = self.sharpe_ratio()
        # Добавьте здесь вызовы других метрик по мере необходимости

    def profit_factor(self):
        total_profit = self.statistics.total_profit
        total_loss = abs(self.statistics.total_loss)  # Убытки могут быть отрицательными, поэтому берем модуль
        return total_profit / total_loss if total_loss != 0 else float('inf')

    def sharpe_ratio(self, risk_free_rate=0.0):
        total_profit = self.statistics.total_profit
        total_trades = self.statistics.total_trades
        if total_trades == 0:
            return 0.0
        avg_return = total_profit / total_trades
        return_std_dev = self.return_std_dev()
        if return_std_dev == 0:
            return 0.0
        return (avg_return - risk_free_rate) / return_std_dev

    def return_std_dev(self):
        profits = [deal.profit for deal in self.statistics.deals]
        avg_profit = sum(profits) / len(profits) if profits else 0.0
        variance = sum((profit - avg_profit) ** 2 for profit in profits) / len(profits) if profits else 0.0
        return math.sqrt(variance)

    def add_custom_metric(self, name, function):
        self.metrics[name] = function(self.statistics)

    def get_metrics(self):
        return self.metrics

    def print_metrics(self):
        for key, value in self.metrics.items():
            print(f"{key}: {value}")
