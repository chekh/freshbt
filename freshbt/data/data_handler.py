import pandas as pd
from .interfaces import IDataHandler

class DataHandler(IDataHandler):
    def __init__(self, data_source):
        self.data_source = data_source
        self.current_bar_index = 0
        self.data = self.load_data(data_source)
    
    def load_data(self, data_source):
        # Загрузка данных с использованием pandas
        return pd.read_csv(data_source)
    
    def get_next_bar(self):
        # Получение следующего бара из данных
        bar = self.data.iloc[self.current_bar_index]
        self.current_bar_index += 1
        return bar
    
    def has_more_data(self):
        # Проверка наличия еще данных для обработки
        return self.current_bar_index < len(self.data)
    
    def get_lower_timeframe_bars(self, current_bar):
        # Получение данных свечей меньшего таймфрейма
        return self.data[self.current_bar_index-5:self.current_bar_index]  # Пример среза данных
