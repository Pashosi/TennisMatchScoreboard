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
        """
        Добавление очка игроку.
        :param point: Словарь с информацией кому добавлять очки. {'name': имя, 'value': поинты}.
        :raises ValueError: Если матч уже завершен.
        """
        if self.winner:
            raise ValueError('Матч уже завершен')

        player_name = point['name']

        if player_name == 'player1':
            self.player1_score_point += int(point['value'])

            self.process_points(player_name)

            # геймы
            if self.player1_score_game == 6 and self.player2_score_game < 5:  # счет 6:<=4
                self.player1_score_set += 1
                self.reset_score_games()
            elif self.player1_score_game == 7 and self.player2_score_game in [5, 6]:  # счет 7:5, 7:6
                self.player1_score_set += 1
                self.reset_score_games()
                self.tiebreak = False
            elif self.player1_score_game == 6 and self.player2_score_game == 6:  # счет 6:6
                self.tiebreak = True

            self.check_match_winner()

        elif player_name == 'player2':
            self.player2_score_point += int(point['value'])

            self.process_points(player_name)

            # геймы
            if self.player2_score_game == 6 and self.player1_score_game < 5:
                self.player2_score_set += 1
                self.reset_score_games()
            elif self.player2_score_game == 7 and self.player1_score_game in [5, 6]:
                self.player2_score_set += 1
                self.reset_score_games()
                self.tiebreak = False
            elif self.player2_score_game == 6 and self.player1_score_game == 6:
                self.tiebreak = True

            self.check_match_winner()

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

    def reset_score_points(self):
        """Очистка полей счета поинтов"""
        self.player1_score_point = 0
        self.player2_score_point = 0

    def reset_score_games(self):
        """Очистка полей счета геймов"""
        self.player1_score_game = 0
        self.player2_score_game = 0

    def check_match_winner(self):
        """Проверка победителя матча"""
        if self.player1_score_set == 2:
            self.winner = self.player1
            # print(f'Победитель: {self.winner}')
        elif self.player2_score_set == 2:
            self.winner = self.player2
            # print(f'Победитель: {self.winner}')


    def process_points(self, player):
        """Обработка поинтов и геймов"""
        if player == 'player1':
            opponent_points = self.player2_score_point
            player_points = self.player1_score_point
        else:
            opponent_points = self.player1_score_point
            player_points = self.player2_score_point

        # Проверка на выигрыш гейма
        if not self.tiebreak:
            if player_points == 5 and opponent_points == 3:  # AD:40
                self.add_point_game(player)
            elif player_points > 3 > opponent_points:  # 40:меньше
                self.add_point_game(player)
            elif player_points == 4 and opponent_points == 4:  # 40:40
                self.player1_score_point = 3
                self.player2_score_point = 3

        # тайбрейк
        elif self.tiebreak:
            if player_points == 7 and opponent_points <= 5 and self.tiebreak:
                self.add_point_game(player)
                self.reset_score_points()
            elif player_points > 7 and opponent_points <= int(player_points) - 2:
                self.add_point_game(player)
                self.reset_score_points()

    def add_point_game(self, player: str):
        """Добавление поинта в гейм"""
        if player == 'player1':
            self.player1_score_game += 1
        else:
            self.player2_score_game += 1

        self.reset_score_points()

