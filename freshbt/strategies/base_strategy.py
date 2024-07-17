from .interfaces import IStrategy

class Strategy(IStrategy):
    def __init__(self, broker):
        self.broker = broker
    
    def update(self, current_bar):
        # Обновление стратегии на основе текущего бара
        pass
    
    def generate_orders(self):
        # Генерация новых ордеров на основе стратегии
        return []
