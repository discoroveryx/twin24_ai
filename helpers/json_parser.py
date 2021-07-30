"""Инструменты парсинга json"""

import json

from typing import Dict
from typing import Generator
from typing import List


class JsonFileParser:
    """
    Парсер json файлов

    метод to_list: возвращает list
    """

    def __init__(self, path_to_files: str):

        # путь до файлов
        self.path_to_files = path_to_files

    def _parse_files(
        self,
        depth=6
    ) -> Generator:
        """Извлекает список файлов из каталога"""

        return (f'{self.path_to_files}/{i}.json' for i in range(1, depth))

    def _json_file_to_dict(self, filename: str) -> dict:
        """Преобразует json файл в dict"""

        # f = open(filename, encoding='utf-8')
        # data = json.load(f)
        # f.close()

        with open(filename, encoding='utf-8') as file:
            data = json.load(file)
            return data

    def to_list(self) -> List[List[Dict]]:
        """JSON to list"""

        mylist: list = []

        for i in self._parse_files():
            data = self._json_file_to_dict(i)
            mylist.append(data)

        return mylist
