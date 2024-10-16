from jinja2 import Template

from src.db.create_db_and_tables import MatchesModel


class TennisMatch:

    def __init__(self, data_match: MatchesModel):
        self.uuid = data_match.uuid
        self.player1 = data_match.player1
        self.player2 = data_match.player2
        self.player1_fk = data_match.player1_fk
        self.player2_fk = data_match.player2_fk
        self.player1_score_game = data_match.score['player1']['games']
        self.player2_score_game = data_match.score['player2']['games']
        self.player1_score_set = data_match.score['player1']['sets']
        self.player2_score_set = data_match.score['player2']['sets']
        self.player1_score_point = data_match.score['player1']['points']
        self.player2_score_point = data_match.score['player2']['points']
        self.winner = data_match.winner


    def add_point(self, point):
        if point['name'] == 'player1':
            self.player1_score_point += int(point['value'])
        elif point['name'] == 'player2':
            self.player2_score_point += int(point['value'])

