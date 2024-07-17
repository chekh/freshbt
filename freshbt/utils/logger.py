from .interfaces import ILogger

class Logger(ILogger):
    def log_results(self, broker, current_bar):
        print(f"Time: {broker.get_current_time()}, Balance: {broker.balance}, Equity: {broker.equity}")
