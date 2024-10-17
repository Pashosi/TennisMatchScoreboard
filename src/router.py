from urllib.parse import urlencode

from src import config
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
    #     self.path = environ.get('PATH_INFO', '/').lstrip('/')
    #     self.method = environ.get('REQUEST_METHOD', 'GET')

    def __call__(self, method: str, path: str):
        status = '200 OK'
        headers = [('Content-type', 'text/html; charset=utf-8'), ]

        if method == 'GET':
            if path == config.paths_list['new_match']:
                request = request_template(self.start_response, status, headers, NewMatchHandler)
                return request
            elif path == config.paths_list['index']:
                request = request_template(self.start_response, status, headers, IndexHandler)
                return request
            elif path == config.paths_list['matches']:
                request = request_template(self.start_response, status, headers, MatchesHandler)
                return request
            elif path.startswith(config.paths_list['match_score']):
                # получаем uuid
                uuid = self.environ.get('QUERY_STRING', '').split('=')[1]
                # загружаем данные матча
                # controller = Controller()
                match = self.unfinished_matches.get(uuid)
                n = 1
                request = request_template(self.start_response, status, headers, MatchScoreGetHandler, match)
                return request

        elif method == 'POST':
            if path == config.paths_list['new_match']:
                controller = Controller()
                data_form = controller.new_match(self.environ)
                n = 2
                # Создаем экземпляр матча
                instance_match = TennisMatch(data_form)
                self.unfinished_matches[instance_match.uuid] = instance_match
                n = 1
                # Создаем параметры для редиректа
                query_params = urlencode({'uuid': instance_match.uuid})
                redirect_url = f'{config.paths_list["match_score"]}?{query_params}'

                # После обработки данных делаем редирект
                status = '302 Found'
                headers = [('Location', redirect_url)]  # Перенаправляем на страницу success
                request = request_template(self.start_response, status, headers)
                return request
            elif path.startswith(config.paths_list['match_score']):
                """Обработчик кнопок матча"""
                # получаем uuid
                uuid = self.environ.get('QUERY_STRING', '').split('=')[1]
                # data_button = self.controller.get_data_match(self.environ)
                # controller = Controller()
                # match = controller.get_match(uuid)

                match = self.unfinished_matches.get(uuid)

                # new_data_match = controller.add_point_match(self.environ, match)

                # добавляем в html измененный экземпляр матча
                request = request_template(self.start_response, status, headers, MatchScorePostHandler, match, self.environ)
                return request
        else:
            status = '404 Not Found'
            headers = [('Content-type', 'text/html; charset=utf-8'), ]
            request = request_template(self.start_response, status, headers, NotFoundHandler)
            return request


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
