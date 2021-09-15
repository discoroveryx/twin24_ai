import requests

import time


class ThrottleRequest:
    """Контекстный менеджер для обработки неудачных попыток запроса."""

    def __init__(self, url_target: str, *, max_retry: int = 5, time_waiting: float = 1.5) -> None:
        """Входные данные."""

        self.url_target = url_target  # url назначения
        self.max_retry = max_retry  # Количество попыток после не удачного ответа
        self.time_waiting = time_waiting  # Время ожидания перед следующей попыткой запроса

    def __enter__(self):
        """
        Не забываем, requests поднимает собственные requests.exceptions.
        """

        # Количество попыток -1, так как в конце метода есть return
        for i in range(self.max_retry - 1):
            # Запрос
            response = requests.get(self.url_target)

            print(f'request retry {i + 1} of {self.max_retry}, status: {response.status_code}')  # noqa

            if response.status_code != 200:
                # Если ответ отрицательный
                # ждем и повторяем запрос на следующей итерации
                # time.sleep блокирует интерпретатор, не самое лучшее решение
                time.sleep(self.time_waiting)
                continue
            else:
                # Если ответ 200, возвращаем результат
                return response

        # Что бы не усложнять выражениями if i < self.max_retry - 1: return
        # просто отдаем последнию попытку
        return requests.get(self.url_target)

    def __exit__(self, type, value, traceback):
        pass
