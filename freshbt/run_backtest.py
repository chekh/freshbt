from backtester import Backtester
from data.data_handler import DataHandler
from strategies.my_strategy import MyStrategy
from broker.hedging_broker import HedgingBroker
from utils.logger import Logger

def run_backtest():
    data_handler = DataHandler('path_to_data')
    broker = HedgingBroker(initial_balance=100000, margin_requirement=0.01, leverage=50)
    strategy = MyStrategy(broker)
    logger = Logger()
    
    backtester = Backtester(data_handler, strategy, broker, logger)
    backtester.run()

if __name__ == "__main__":
    run_backtest()
