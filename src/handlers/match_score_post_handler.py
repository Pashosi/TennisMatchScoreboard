from urllib.parse import parse_qs

from jinja2 import Template

from src import config
from src.db.create_db_and_tables import MatchesModel
from src.service.tennis_match import TennisMatch


class MatchScorePostHandler:

    def __init__(self, match: TennisMatch, environ):
        self.match = match
        self.environ = environ

    def __call__(self):
        with open(f'{config.paths_list["templates_files"]}{config.paths_list["match_score"]}', 'rb') as file:
            content_before = file.read().decode('utf-8')

            request_uri = f'{config.paths_list["templates_files"]}' \
                          f'{config.paths_list["match_score"]}?uuid={self.match.uuid}'

            self.add_point_match(self.environ, self.match)

            temlate = Template(content_before)

            content_afer = temlate.render(
                request_uri=request_uri,
                uuid=self.match.uuid,
                player1=self.match.player1,
                player2=self.match.player2,
                player1_sets=self.match.player1_score_set,
                player2_sets=self.match.player2_score_set,
                player1_games=self.match.player1_score_game,
                player2_games=self.match.player2_score_game,
                player1_points=self.match.player1_score_point,
                player2_points=self.match.player2_score_point
            )
            return content_afer

    def add_point_match(self, environ, match):
        """Добавление поинта в матч"""
        point = self.get_data_match(environ)

        request = match.add_point(point)
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
