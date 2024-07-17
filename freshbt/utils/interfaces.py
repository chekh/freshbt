from abc import ABC, abstractmethod

class ICommissionCalculator(ABC):
    @abstractmethod
    def calculate(self, volume, price):
        pass

class ILogger(ABC):
    @abstractmethod
    def log_results(self, broker, current_bar):
        pass
