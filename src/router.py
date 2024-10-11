from urllib.parse import urlencode

from src import config
from src.controller import Controller
from src.handlers.match_score_handler import MatchScoreHandler


class Router:
    def __init__(self, environ, start_response):
        self.environ = environ
        self.start_response = start_response
        self.controller = Controller()
    #     self.path = environ.get('PATH_INFO', '/').lstrip('/')
    #     self.method = environ.get('REQUEST_METHOD', 'GET')

    def __call__(self, method: str, path: str):
        if method == 'GET':
            if path == config.paths_list['new_match']:
                request = self.render_template(config.paths_list['new_match'], self.start_response)
                return request
            elif path == config.paths_list['index']:
                request = self.render_template(config.paths_list['index'], self.start_response)
                return request
            elif path == config.paths_list['matches']:
                request = self.render_template(config.paths_list['matches'], self.start_response)
                return request
            elif path.startswith(config.paths_list['match_score']):
                # получаем uuid
                uuid = self.environ.get('QUERY_STRING', '').split('=')[1]
                # загружаем данные матча
                data_match = self.controller.get_data_match_score(uuid)

                handler = MatchScoreHandler(data_match)
                request = handler()
                response_headers = [("Content-type", "text/html; charset=utf-8"), ]
                self.start_response('200 OK', response_headers)

                html_as_bytes = request.encode("utf-8")
                n = 1
                # request = self.render_template(config.paths_list['match_score'], self.start_response, d)
                n = 1
                return [html_as_bytes]

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
                self.start_response(status, headers)
                return []
        else:
            self.start_response('404 Not Found', [])
            return ['404 Not Found']


    def render_template(self, path, start_response, data=None):
        """Загрузка HTML-шаблона"""
        with open(f'{config.paths_list["templates_files"]}{path}', 'rb') as file:

            content = file.read().decode('utf-8')
            if data:
                html_content = f'{data}'
                content = content.replace('{{ html_content }}', html_content)
            if content:
                start_response('200 OK', [])
                return [content.encode()]
            else:
                start_response('404 Not Found', [('Content-Type', 'text/html;charset=utf-8')])
                return [b'404 Not Found']
