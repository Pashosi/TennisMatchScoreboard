import os

from jinja2 import Template

import config
from src.service.tennis_match import TennisMatch


class MatchScoreGetHandler:
    def __init__(self, match: TennisMatch):
        self.match = match

    def __call__(self):
        with open(os.path.join(config.BASE_DIR, "view", "templates", "match-score.html"), 'rb') as file:
            content_before = file.read().decode('utf-8')

            request_uri = f'{os.path.join(config.BASE_DIR, "view", "templates", "match-score.html")}' \
                          f'?uuid={self.match.uuid}'

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
                player1_points=self.translate_point(self.match.player1_score_point, self.match.tiebreak),
                player2_points=self.translate_point(self.match.player2_score_point, self.match.tiebreak),
                winner=self.match.winner
            )
            return content_afer

    def translate_point(self, number, tiebreak=None):
        """Перевод очков из цифры в число"""
        if tiebreak:
            return number
        sup_dict = {
            0: '0',
            1: '15',
            2: '30',
            3: '40',
            4: 'AD',
        }

        return sup_dict[number]
