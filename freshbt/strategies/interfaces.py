from abc import ABC, abstractmethod

class IStrategy(ABC):
    @abstractmethod
    def update(self, current_bar):
        pass
    
    @abstractmethod
    def generate_orders(self):
        pass
