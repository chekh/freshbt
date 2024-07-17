class BacktestStatistics:
    def __init__(self):
        self.total_trades = 0
        self.profit_trades = 0
        self.loss_trades = 0
        self.long_trades = 0
        self.short_trades = 0
        self.total_profit = 0.0
        self.total_loss = 0.0
        self.max_drawdown = 0.0
        self.max_balance = 0.0
        self.current_drawdown = 0.0
        self.largest_profit_trade = 0.0
        self.largest_loss_trade = 0.0
        self.deals = []  # Список сделок

    def update(self, deal):
        self.total_trades += 1
        self.deals.append(deal)

        if deal.profit >= 0:
            self.profit_trades += 1
            self.total_profit += deal.profit
            if deal.profit > self.largest_profit_trade:
                self.largest_profit_trade = deal.profit
        else:
            self.loss_trades += 1
            self.total_loss += deal.profit
            if deal.profit < self.largest_loss_trade:
                self.largest_loss_trade = deal.profit

        if deal.deal_type == "buy":
            self.long_trades += 1
        elif deal.deal_type == "sell":
            self.short_trades += 1

        self.update_drawdown(deal)

    def update_drawdown(self, deal):
        current_balance = deal.profit + self.total_profit + self.total_loss
        if current_balance > self.max_balance:
            self.max_balance = current_balance
        self.current_drawdown = self.max_balance - current_balance
        if self.current_drawdown > self.max_drawdown:
            self.max_drawdown = self.current_drawdown

    def get_statistics(self):
        return {
            "total_trades": self.total_trades,
            "profit_trades": self.profit_trades,
            "loss_trades": self.loss_trades,
            "long_trades": self.long_trades,
            "short_trades": self.short_trades,
            "total_profit": self.total_profit,
            "total_loss": self.total_loss,
            "largest_profit_trade": self.largest_profit_trade,
            "largest_loss_trade": self.largest_loss_trade,
            "max_drawdown": self.max_drawdown
        }

    def print_statistics(self):
        stats = self.get_statistics()
        for key, value in stats.items():
            print(f"{key}: {value}")
