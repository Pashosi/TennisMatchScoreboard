from urllib.parse import parse_qs


class Controller:
    def __init__(self, environ, start_response):
        self.environ = environ
        self.start_response = start_response

    def get_data_form(self):
        response_body = int(self.environ.get('CONTENT_LENGTH', 0))
        body = self.environ['wsgi.input'].read(response_body).decode('utf-8')
        post_data = parse_qs(body)

        # Извлекаем данные формы (имя и сообщение)
        name1 = post_data.get('name1', [''])[0]
        name2 = post_data.get('name2', [''])[0]
        print(name1, name2, sep=': ')
        self.start_response('204 No Content', [])  # TODO: добавить функционал
        return []