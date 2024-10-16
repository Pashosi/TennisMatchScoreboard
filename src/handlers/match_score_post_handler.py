from urllib.parse import parse_qs

from jinja2 import Template

from src import config
from src.db.create_db_and_tables import MatchesModel
from src.service.tennis_match import TennisMatch


class MatchScorePostHandler:

    def __init__(self, environ, match: MatchesModel):
        self.match = TennisMatch(match)

    def __call__(self):
        pass

    def add_point_match(self, environ):
        """Добавление поинта в матч"""
        point = self.get_data_match(environ)

        request = self.match.add_point(point)
        return request

    def get_data_match(self, environ):
        """Получение данных из кнопки матча"""
        response_body = int(environ.get('CONTENT_LENGTH', 0))
        body = environ['wsgi.input'].read(response_body).decode('utf-8')
        post_data = parse_qs(body)

        # Извлекаем данные формы (имя и сообщение)
        n = 1
        name = next(iter(post_data))
        value = post_data[name][0]
        return {'name': name, 'value': value}