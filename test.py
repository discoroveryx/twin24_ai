import unittest
from unittest import mock

from helpers.throttle_request import ThrottleRequest


class ThrottleTestCase(unittest.TestCase):
    """Тест кейс контекстного менеджера ThrottleRequest."""

    @mock.patch('helpers.throttle_request.requests.get')
    def test_throttle(self, requests_get):
        """Первые два запроса отдают 429, последний 200."""

        # Подготавливаем 200 OK ответ
        response_mock_200 = mock.Mock()
        response_mock_200.status_code = 200

        # Подготавливаем 429 Too Many Requests ответ
        response_mock_429 = mock.Mock()
        response_mock_429.status_code = 429

        # Два ответа 429 + один 200
        requests_get.side_effect = [response_mock_429, response_mock_429, response_mock_200]

        url = 'https://sandbox.twin24.ai/parse?q=здравствуйте'

        with ThrottleRequest(url, max_retry=5, time_waiting=0.1) as response:
            print(response.status_code)  # noqa
            self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
