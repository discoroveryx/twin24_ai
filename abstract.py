from abc import ABC
from abc import abstractmethod


class GraphBuilder(ABC):
    """Строитель графа"""

    @abstractmethod
    def pipe_parse(self):
        """
        Парсим json файлы
        """

    @abstractmethod
    def pipe_get_intent(self, pipe_data):
        """Забираем намерения"""

    @abstractmethod
    def pipe_normalization(self, pipe_data):
        """Нормализуем данные"""

    @abstractmethod
    def pipe_build_graph(self, pipe_data):
        """Строим граф"""

    @abstractmethod
    def get_graph(self):
        """Получаем граф"""
