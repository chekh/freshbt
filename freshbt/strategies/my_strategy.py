from .base_strategy import Strategy

class MyStrategy(Strategy):
    def update(self, current_bar):
        # Реализация обновления стратегии
        pass
    
    def generate_orders(self):
        # Реализация генерации новых ордеров
        return []
