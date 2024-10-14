from urllib.parse import urlencode

from src import config
from src.controller import Controller
from src.handlers.index_handler import IndexHandler
from src.handlers.match_score_handler import MatchScoreHandler
from src.handlers.matches_handler import MatchesHandler
from src.handlers.new_match_handler import NewMatchHandler
from src.handlers.not_found_handler import NotFoundHandler


class Router:
    def __init__(self, environ, start_response):
        self.environ = environ
        self.start_response = start_response
        self.controller = Controller()

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
                match = self.controller.get_match_score(uuid)

                request = request_template(self.start_response, status, headers, MatchScoreHandler, match)
                return request

        elif method == 'POST':
            if path == config.paths_list['new_match']:
                data_form = self.controller.new_match(self.environ)
                n = 1
                # Создаем параметры для редиректа
                query_params = urlencode({'uuid': data_form.uuid})
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
                match = self.controller.get_match_score(uuid)
                new_data_match = self.controller.add_point_match(self.environ, match)

                # добавляем в html измененный экземпляр матча
                request = request_template(self.start_response, status, headers, MatchScoreHandler, new_data_match)
                return request
        else:
            status = '404 Not Found'
            headers = [('Content-type', 'text/html; charset=utf-8'), ]
            request = request_template(self.start_response, status, headers, NotFoundHandler)
            return request


def request_template(start_response, status, response_headers, class_handler=None, data=None):
    """Формируем html и возвращаем его"""
    if not class_handler:  # случай когда просто нужен редирект
        start_response(status, response_headers)
        return []
    if data:  # если есть данные, то передаем в обработчик
        handler = class_handler(data)
    else:
        handler = class_handler()
    request = handler()
    start_response(status, response_headers)

    html_as_bytes = request.encode("utf-8")
    return [html_as_bytes]
