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
            player1_score = self.data_match.score['player1']
            player2_score = self.data_match.score['player2']

            temlate = Template(content_before)

            content_afer = temlate.render(
                request_uri=request_uri,
                player1=player1,
                player2=player2,
                player1_score=player1_score,
                player2_score=player2_score
            )
            return content_afer
