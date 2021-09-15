"""Инструменты парсинга json."""

import json
from dataclasses import dataclass
from typing import Dict, Generator, List


@dataclass(init=True, repr=False, eq=False)
class JsonFileParser:
    """
    Парсер json файлов.

    метод to_list: возвращает list
    """

    path_to_files: str  # Путь до файлов

    def _parse_files(
        self,
        depth: int = 6,
    ) -> Generator:
        """Извлекает список файлов из каталога."""

        return (f'{self.path_to_files}/{i}.json' for i in range(1, depth))

    def _json_file_to_dict(self, filename: str) -> dict:
        """Преобразует json файл в dict."""

        with open(filename, encoding='utf-8') as file:
            data = json.load(file)
            return data

    def to_list(self) -> List[List[Dict]]:
        """JSON to list."""

        mylist: list = []

        for i in self._parse_files():
            data = self._json_file_to_dict(i)
            mylist.append(data)

        return mylist
