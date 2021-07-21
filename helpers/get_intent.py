from helpers.throttle_request import ThrottleRequest


class GetIntent:
    """Определяем намерение из ответа человека"""

    @staticmethod
    def get_intent(human_text: str) -> str:
        """
        Забираем намерения
        """

        # в нижний регистр
        human_text = human_text.lower()

        url = f'https://sandbox.twin24.ai/parse?q={human_text}'
        # print(url)

        with ThrottleRequest(url, max_retry=5, time_waiting=0.5) as response:
            print(f'human_text = {human_text}')  # noqa
            # print(response)
            # print(human_text, response.status_code)  # noqa

            if response.status_code == 200:
                result = response.json()
                # print(result)

                if 'intent' in result:
                    if 'name' in result['intent']:
                        intent_name = result['intent']['name']
                        # print(result['intent']['name'], human_text)

                        return intent_name

        raise ValueError
