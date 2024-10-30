from urllib.parse import urlencode, parse_qs

import config
from src.controller import Controller
from src.handlers.index_handler import IndexHandler
from src.handlers.match_score_get_handler import MatchScoreGetHandler
from src.handlers.match_score_post_handler import MatchScorePostHandler
from src.handlers.matches_handler import MatchesHandler
from src.handlers.new_match_handler import NewMatchHandler
from src.handlers.not_found_handler import NotFoundHandler
from src.service.tennis_match import TennisMatch


class Router:
    def __init__(self, environ, start_response):
        self.environ = environ
        self.start_response = start_response

    unfinished_matches = {}  # словарь не завершенных матчей

    def __call__(self, method: str, path: str):
        status = '200 OK'
        headers = [('Content-type', 'text/html; charset=utf-8'), ]

        if method == 'GET':
            if path == config.paths_list['new_match'][:-5]:  # new-match
                request = request_template(self.start_response, status, headers, NewMatchHandler)
                return request
            elif path == config.paths_list['index'][:-5]:  # index
                request = request_template(self.start_response, status, headers, IndexHandler)
                return request
            elif path.startswith(config.paths_list['matches'][:-5]):  # matches
                n = 1
                query_string = self.environ.get('QUERY_STRING')
                params = parse_qs(query_string)

                # достаем параметры страницы
                page = int(params.get('page', [1])[0])  # номер страницы или 1 если нет

                search_query = params.get('search', [''])[0]  # параметр фильтрации, если есть

                data = {'page': page, 'search': search_query}
                request = request_template(self.start_response, status, headers, MatchesHandler, match=data)
                return request
            elif path.startswith(config.paths_list['match_score'][:-5]):  # match-score
                # получаем uuid
                uuid = self.environ.get('QUERY_STRING', '').split('=')[1]

                if len(uuid) != 36:  # если не правильный uuid
                    request = request_not_found(self.start_response)
                    return request

                # загружаем данные матча
                match = self.unfinished_matches.get(uuid)

                if not match:
                    data = Controller.get_match(uuid)
                    match = TennisMatch(data)
                request = request_template(self.start_response, status, headers, MatchScoreGetHandler, match)
                return request
            else:
                request = request_not_found(self.start_response)
                return request

        elif method == 'POST':
            if path == config.paths_list['new_match'][:-5]:  # new-match
                controller = Controller()
                data_form = controller.new_match(self.environ)

                # Создаем экземпляр матча
                instance_match = TennisMatch(data_form)
                self.unfinished_matches[instance_match.uuid] = instance_match

                # Создаем параметры для редиректа
                query_params = urlencode({'uuid': instance_match.uuid})
                redirect_url = f'{config.paths_list["match_score"][:-5]}?{query_params}'

                # После обработки данных делаем редирект
                status = '302 Found'
                headers = [('Location', redirect_url)]  # Перенаправляем на страницу success
                request = request_template(self.start_response, status, headers)
                return request
            elif path.startswith(config.paths_list['match_score'][:-5]):
                """Обработчик кнопок матча"""
                # получаем uuid
                uuid = self.environ.get('QUERY_STRING', '').split('=')[1]
                match = self.unfinished_matches.get(uuid)
                if match is None:
                    raise Exception('Не найден матч')

                # добавляем в html измененный экземпляр матча
                request = request_template(self.start_response, status, headers, MatchScorePostHandler, match,
                                           self.environ)
                if match.winner:
                    self.delete_unfinished_match(uuid)
                return request

            else:
                request = request_not_found(self.start_response)
                return request
        else:
            request = request_not_found(self.start_response)
            return request

    def delete_unfinished_match(self, uuid):
        self.unfinished_matches.pop(uuid)
        print(f'Матч {uuid} удален')


def request_template(start_response, status, response_headers, class_handler=None, match=None, environ=None):
    """Формируем html и возвращаем его"""
    if not class_handler:  # случай когда просто нужен редирект
        start_response(status, response_headers)
        return []
    if match and not environ:  # если есть данные, то передаем в обработчик
        handler = class_handler(match)
    elif match and environ:
        handler = class_handler(match, environ)
    else:
        handler = class_handler()
    request = handler()
    start_response(status, response_headers)

    html_as_bytes = request.encode("utf-8")
    return [html_as_bytes]


def request_not_found(start_response):
    """Формируем html страницы неверного запроса и возвращаем его"""
    status = '404 Not Found'
    headers = [('Content-type', 'text/html; charset=utf-8'), ]
    request = request_template(start_response, status, headers, NotFoundHandler)
    return request
