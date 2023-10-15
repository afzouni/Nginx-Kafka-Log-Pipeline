from collections import defaultdict
import threading
from logging_config import logger

class Metrics:
    def __init__(self):
        self._counter = 0
        self._sum = 0
        self._min = float('inf')
        self._max = float('-inf')

    def add_response(self, value: float):
        self._counter += 1
        self._sum += value
        self._update_max(value)
        self._update_min(value)

    def _update_max(self, value: float):
        self._max = max(self._max, value)

    def _update_min(self, value: float):
        self._min = min(self._min, value)

    def get_metrics(self):
        return {
            "counter": self._counter,
            "sum": self._sum,
            "min": self._min,
            "max": self._max,
            "average": self._calculate_average()
        }

    def _calculate_average(self):
        if self._counter == 0:
            return 0
        return self._sum / self._counter 

class MetricsManager:
    def __init__(self):
        self.hourly_metrics = defaultdict(lambda: defaultdict(Metrics))
        self.__lock = threading.Lock()
    
    def _validate_datetime(self, datetime_str: str):
        if 'T' in datetime_str:
            date, time = datetime_str.split('T') 
            hour = time.split(':')[0]  
        else:
            raise Exception('Invalid datetime format')
        return date, hour


    def record_response(self, datetime_str: str, response_time: float):
        date, hour = self._validate_datetime(datetime_str)
        with self.__lock:
            self.hourly_metrics[date][hour].add_response(response_time)
            logger.debug("Stored response for datetime %s - Response Time: %s", datetime_str, response_time)

    def metrics(self, datetime_str: str):        
        date, hour = self._validate_datetime(datetime_str)
        if date in self.hourly_metrics and hour in self.hourly_metrics[date]:
            return self.hourly_metrics[date][hour].get_metrics()
        else:
            logger.warning("No data available for the specified datetime: %s", datetime_str)
            raise Exception('No data available for the specified datetime.')
