from src import config
from src.controller import Controller


class Router:
    def __init__(self, environ, start_response):
        self.environ = environ
        self.start_response = start_response
        self.controller = Controller(self.environ, self.start_response)
    #     self.path = environ.get('PATH_INFO', '/').lstrip('/')
    #     self.method = environ.get('REQUEST_METHOD', 'GET')

    def __call__(self, method: str, path: str):
        if method == 'GET':
            if path == config.path_list['new_match']:
                request = self.render_template(config.path_list['new_match'], self.start_response)
                return request
        elif method == 'POST':
            if path == config.path_list['new_match']:
                data_form = self.controller.get_data_form()

                return data_form
        else:
            self.start_response('404 Not Found', [])
            return ['404 Not Found']


    def render_template(self, path, start_response):
        """Загрузка HTML-шаблона"""
        with open(f'{config.path_list["templates_files"]}{path}', 'rb') as file:
            content = file.read().decode('utf-8')
            if content:
                start_response('200 OK', [('Content-Type', 'text/html;charset=utf-8')])
                return [content.encode()]
            else:
                start_response('404 Not Found', [('Content-Type', 'text/html;charset=utf-8')])
                return [b'404 Not Found']
