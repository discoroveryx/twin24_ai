from helpers.get_intent import GetIntent
from helpers.json_parser import JsonFileParser

import pprint
from typing import Dict
from typing import List

from abstract import GraphBuilder

pp = pprint.PrettyPrinter(indent=2, depth=10, compact=True)


class GraphBuilderVersion1(GraphBuilder):
    """
    Строитель графа

    Цель:
        Построить дерево разговора для определния реакции (намерения) на фразы бота

    Реализация:
        Распарсить json диалоги
        Забираем намерения с помощью стороннего сервиса sandbox.twin24.ai
        Отсекаем первое сообщение, если это человек
        В основном обработчике складываем результат
    """

    def _get_last_position_of_common_pipe(self, object_list: list) -> list:
        """Получить последнию свободную позицию в общем pipe"""

        if object_list:
            for i in object_list:
                if 'replies' in i:
                    # рекурсивный вызов
                    res = self._get_last_position_of_common_pipe(i['replies'])
                else:
                    res = i
        else:
            res = object_list
        return res

    def pipe_parse(self) -> List[List[Dict]]:
        """
        Парсим json файлы

        Результат:
            - общий list
        """

        parser = JsonFileParser('dialogs')

        return parser.to_list()

    def pipe_get_intent(self, pipe_data: list) -> list:
        """Забираем намерения"""

        for head in pipe_data:
            for i in head:
                if i['is_bot'] is True:
                    i['intent'] = 'bot'

                if i['is_bot'] is False:
                    i['intent'] = GetIntent.get_intent(i['text'])

        return pipe_data

    def pipe_normalization(self, pipe_data: list) -> list:
        """Отсекаем первое сообщение в каждом диалоге, если это человек"""

        for head in pipe_data:
            if head[0]['is_bot'] is False:
                head.pop(0)

        return pipe_data

    def pipe_build_graph(self, pipe_data: list) -> list:
        """Строим граф"""

        common_pipe: list = []

        for head in pipe_data:
            position = 1
            for i in head:
                # print('is_bot', i['is_bot'], position)  # noqa

                if i['is_bot']:
                    tmp = {
                        'is_bot': True,
                        'phrases': [i['text'], ],
                        'replies': [],
                    }
                    if position == 1:
                        if bool(common_pipe) is False:
                            common_pipe.append(tmp)
                        else:
                            common_pipe[0]['phrases'].append(i['text'])
                    else:
                        common_pipe_position = self._get_last_position_of_common_pipe(common_pipe)
                        common_pipe_position.append(tmp)
                else:
                    tmp = {
                        'is_bot': False,
                        'intent': i['intent'],
                        'phrases': [i['text'], ],
                        'replies': [],
                    }
                    if position == 2:
                        common_pipe[0]['replies'].append(tmp)
                    else:
                        common_pipe_position = self._get_last_position_of_common_pipe(common_pipe)
                        common_pipe_position.append(tmp)
                position = position + 1

        return common_pipe

    def get_graph(self) -> list:
        """Запускаем обработчик"""

        pipe_data = self.pipe_parse()
        pipe_data = self.pipe_get_intent(pipe_data)
        pipe_data = self.pipe_normalization(pipe_data)
        pipe_data = self.pipe_build_graph(pipe_data)

        return pipe_data


if __name__ == '__main__':
    graph_builder = GraphBuilderVersion1()

    graph_result = graph_builder.get_graph()

    pp.pprint(graph_result)
