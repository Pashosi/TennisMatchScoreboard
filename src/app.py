from whitenoise import WhiteNoise

from src import config
from waitress import serve

from src.router import Router


def app(environ, start_response):
    # Определяем путь запроса
    path = environ.get('PATH_INFO', '/').lstrip('/')
    # Метод запроса
    method = environ.get('REQUEST_METHOD', 'GET')

    if path == 'favicon.ico':
        # Игнорируем запрос на favicon.ico, возвращаем код 204 (No Content)
        start_response('204 No Content', [])
        return []

    router = Router(environ, start_response)
    response = router(method, path)
    return response


if __name__ == '__main__':
    application = WhiteNoise(app, config.path_list['static_files'])
    serve(application, host='localhost', port=8080)
