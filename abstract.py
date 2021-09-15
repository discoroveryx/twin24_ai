from abc import ABC, abstractmethod
from typing import Dict, List


class GraphBuilder(ABC):
    """Строитель графа."""

    @abstractmethod
    def pipe_parse(self) -> List[List[Dict]]:
        """Парсим json файлы."""

    @abstractmethod
    def pipe_get_intent(self, pipe_data: list) -> list:
        """Забираем намерения."""

    @abstractmethod
    def pipe_normalization(self, pipe_data: list) -> list:
        """Нормализуем данные."""

    @abstractmethod
    def pipe_build_graph(self, pipe_data: list) -> list:
        """Строим граф."""

    @abstractmethod
    def get_graph(self) -> list:
        """Получаем граф."""
