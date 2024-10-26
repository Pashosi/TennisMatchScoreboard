import os

from jinja2 import Template

import config
from src.model import Model


class MatchesHandler:

    def __init__(self, data: dict):
        self.page = data['page']
        self.search = data['search']

    def __call__(self):
        with open(os.path.join(config.BASE_DIR, "view", "templates", "matches.html"), 'rb') as file:
            content_before = file.read().decode('utf-8')

            request_uri = os.path.join(config.BASE_DIR, "view", "templates", "matches.html")

            model = Model()

            # Если поиск включен
            if self.search:
                try:
                    num_player = model.get_player(self.search).id
                    matches = model.get_matches(filter=num_player)
                except Exception:
                    matches = []
            else:
                matches = model.get_matches()

            list_winner_players = sorted(set(model.get_players_winner_matches()))  # список игроков с победами

            list_matches, pages = self.paginate_data(matches, int(self.page), 4)
            temlate = Template(content_before)

            content_afer = temlate.render(
                request_uri=request_uri,
                matches=list_matches,
                list_winner_players=list_winner_players,
                search_query=self.search,
                page=int(self.page),
                pages=pages,
            )
            return content_afer

    def paginate_data(self, data, page, per_page):
        start = (page - 1) * per_page
        end = start + per_page
        return data[start:end], len(data) // per_page + (1 if len(data) % per_page else 0)