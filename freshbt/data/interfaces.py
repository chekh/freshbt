from abc import ABC, abstractmethod

class IDataHandler(ABC):
    @abstractmethod
    def load_data(self, data_source):
        pass

    @abstractmethod
    def get_next_bar(self):
        pass

    @abstractmethod
    def has_more_data(self):
        pass

    @abstractmethod
    def get_lower_timeframe_bars(self, current_bar):
        pass
