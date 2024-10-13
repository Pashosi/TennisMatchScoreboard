from jinja2 import Template

from src import config


class MatchScoreHandler:
    def __init__(self, data_match):
        self.data_match = data_match

    def __call__(self):
        with open(f'{config.paths_list["templates_files"]}{config.paths_list["match_score"]}', 'rb') as file:
            content_before = file.read().decode('utf-8')

            request_uri = f'{config.paths_list["templates_files"]}' \
                          f'{config.paths_list["match_score"]}?uuid={self.data_match.uuid}'
            player1 = self.data_match.player1
            player2 = self.data_match.player2
            player1_sets = self.data_match.score['player1']['sets']
            player2_sets = self.data_match.score['player2']['sets']
            player1_games = self.data_match.score['player1']['games']
            player2_games = self.data_match.score['player2']['games']
            player1_points = self.data_match.score['player1']['points']
            player2_points = self.data_match.score['player2']['points']



            temlate = Template(content_before)

            content_afer = temlate.render(
                request_uri=request_uri,
                player1=player1,
                player2=player2,
                player1_sets=player1_sets,
                player2_sets=player2_sets,
                player1_games=player1_games,
                player2_games=player2_games,
                player1_points=player1_points,
                player2_points=player2_points
            )
            return content_afer
