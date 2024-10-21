from jinja2 import Template

from src.db.create_db_and_tables import MatchesModel
from src.model import Model


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
        self.tiebreak = None

    def add_point(self, point):
        if self.winner:
            raise ValueError('Матч уже завершен')

        if point['name'] == 'player1':
            self.player1_score_point += int(point['value'])

            if self.player1_score_point == 5 and self.player2_score_point == 3 and not self.tiebreak:  # счет AD:40
                self.player1_score_game += 1
                self.player1_score_point = 0
                self.player2_score_point = 0
            elif self.player1_score_point == 4 and self.player2_score_point == 4 and not self.tiebreak:  # 40->AD:AD
                self.player1_score_point = 3
                self.player2_score_point = 3
            elif self.player1_score_point > 3 > self.player2_score_point and not self.tiebreak:
                self.player1_score_game += 1
                self.player1_score_point = 0
                self.player2_score_point = 0

            # тайбрейк
            elif self.player1_score_point == 7 and self.player2_score_point <= 5 and self.tiebreak:  # счет 7:<=5
                self.player1_score_game += 1
                self.player1_score_point = 0
                self.player2_score_point = 0
            elif self.player1_score_point > 7 and self.player2_score_point <= int(self.player1_score_point) - 2 and self.tiebreak:
                self.player1_score_game += 1
                self.player1_score_point = 0
                self.player2_score_point = 0
            # геймы
            if self.player1_score_game == 6 and self.player2_score_game < 5:  # счет 6:<=4
                self.player1_score_set += 1
                self.player1_score_game = 0
                self.player2_score_game = 0
            elif self.player1_score_game == 7 and self.player2_score_game in [5, 6]:  # счет 7:5, 7:6
                self.player1_score_set += 1
                self.player1_score_game = 0
                self.player2_score_game = 0
                self.tiebreak = False
            elif self.player1_score_game == 6 and self.player2_score_game == 6:  # счет 6:6
                self.tiebreak = True

            # сеты
            if self.player1_score_set == 2 and self.player2_score_set < 2:
                self.winner = self.player1
                print(f'победитель {self.winner}')
        elif point['name'] == 'player2':
            self.player2_score_point += int(point['value'])

            if self.player2_score_point == 5 and self.player1_score_point == 3 and not self.tiebreak:
                self.player2_score_game += 1
                self.player2_score_point = 0
                self.player1_score_point = 0
            elif self.player2_score_point == 4 and self.player1_score_point == 4 and not self.tiebreak:  # счет 40->AD:AD
                self.player2_score_point = 3
                self.player1_score_point = 3
            elif self.player2_score_point > 3 > self.player1_score_point and not self.tiebreak:
                self.player2_score_game += 1
                self.player2_score_point = 0
                self.player1_score_point = 0

            # тайбрейк
            elif self.player2_score_point == 7 and self.player1_score_point <= 5 and self.tiebreak:
                self.player2_score_game += 1
                self.player2_score_point = 0
                self.player1_score_point = 0
            elif self.player2_score_point > 7 and self.player1_score_point <= int(self.player2_score_point) - 2 and self.tiebreak:
                self.player2_score_game += 1
                self.player2_score_point = 0
                self.player1_score_point = 0

            # геймы
            if self.player2_score_game == 6 and self.player1_score_game < 5:
                self.player2_score_set += 1
                self.player2_score_game = 0
                self.player1_score_game = 0
            elif self.player2_score_game == 7 and self.player1_score_game in [5, 6]:
                self.player2_score_set += 1
                self.player2_score_game = 0
                self.player1_score_game = 0
                self.tiebreak = False
            elif self.player2_score_game == 6 and self.player1_score_game == 6:
                self.tiebreak = True

            # сеты
            if self.player2_score_set == 2 and self.player1_score_set < 2:
                self.winner = self.player2
                print(f'победитель {self.winner}')

    def update_match_in_bd(self):
        """Обновление данных матча в БД"""
        model_obj = Model()
        csv_render_score_match = self.rander_match_to_csv()
        model_obj.update_winner_and_score_match(self.uuid, self.winner, csv_render_score_match)

    def rander_match_to_csv(self):
        """Формирование данных для записи результата матча в БД"""
        data = {"player1": {"sets": self.player1_score_set, "games": self.player1_score_game,
                            "points": self.player1_score_point},
                "player2": {"sets": self.player2_score_set, "games": self.player2_score_game,
                            "points": self.player2_score_point}}

        return data
