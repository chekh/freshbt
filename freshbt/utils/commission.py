from .interfaces import ICommissionCalculator

class Commission(ICommissionCalculator):
    def __init__(self, commission_rate=0.0001):
        self.commission_rate = commission_rate  # Ставка комиссии, например, 0.01% от объема сделки

    def calculate(self, volume, price):
        return volume * price * self.commission_rate
