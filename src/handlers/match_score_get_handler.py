from jinja2 import Template

from src import config
from src.model import Model
from src.service.tennis_match import TennisMatch


class MatchScoreGetHandler:
    def __init__(self, match: TennisMatch):
        self.match = match

    def __call__(self):
        with open(f'{config.paths_list["templates_files"]}{config.paths_list["match_score"]}', 'rb') as file:
            content_before = file.read().decode('utf-8')

            request_uri = f'{config.paths_list["templates_files"]}' \
                          f'{config.paths_list["match_score"]}?uuid={self.match.uuid}'

            # player1 = self.match.player1
            # player2 = self.match.player2
            # player1_sets = self.data_match.score['player1']['sets']
            # player2_sets = self.data_match.score['player2']['sets']
            # player1_games = self.data_match.score['player1']['games']
            # player2_games = self.data_match.score['player2']['games']
            # player1_points = self.data_match.score['player1']['points']
            # player2_points = self.data_match.score['player2']['points']
            # uuid = f'uuid={self.data_match.uuid}'



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
