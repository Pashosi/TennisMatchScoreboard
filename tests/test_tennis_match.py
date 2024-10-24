import unittest
from unittest.mock import Mock
from uuid import uuid4

from src.controller import Controller
from src.model import Model
from src.service.tennis_match import TennisMatch


class TestTennisMatch(unittest.TestCase):

    def setUp(self):
        self.match_in_db = Mock()
        self.match_in_db.uuid = str(uuid4())
        self.match_in_db.player1 = 'player1'
        self.match_in_db.player2 = 'player2'
        self.match_in_db.player1_fk = 1
        self.match_in_db.player2_fk = 2
        self.match_in_db.score = {
            'player1': {
                "sets": 0,
                "games": 0,
                "points": 0,
            },
            'player2': {
                "sets": 0,
                "games": 0,
                "points": 0,
            }
        }
        self.match_in_db.winner = None


    def test_game_not_end(self):
        """Проверка условия при счете 40:40"""
        match = TennisMatch(self.match_in_db)
        for _ in range(3):
            match.add_point({'name': 'player1', 'value': 1})
            match.add_point({'name': 'player2', 'value': 1})
        self.assertEqual(3, match.player1_score_point)
        self.assertEqual(3, match.player2_score_point)
        self.assertEqual(0, match.player1_score_game)
        self.assertEqual(0, match.player2_score_game)

    def test_winner_game(self):
        """Проверка на присвоение гейма"""
        match = TennisMatch(self.match_in_db)
        for _ in range(4):
            match.add_point({'name': 'player1', 'value': 1})
        self.assertEqual(1, match.player1_score_game)

    def test_more_less_points(self):
        """Проверка на отображение больше меньше при счете AD:40"""
        match = TennisMatch(self.match_in_db)
        for _ in range(4):
            match.add_point({'name': 'player1', 'value': 1})
            match.add_point({'name': 'player2', 'value': 1})

        match.add_point({'name': 'player1', 'value': 1})
        self.assertEqual(4, match.player1_score_point)
        self.assertEqual(3, match.player2_score_point)


    def test_balancing_more_less_points(self):
        """Проверка на уравнивание при счете AD:40 + поинт второму игроку"""
        match = TennisMatch(self.match_in_db)
        for _ in range(4):
            match.add_point({'name': 'player1', 'value': 1})
            match.add_point({'name': 'player2', 'value': 1})
        self.assertEqual(3, match.player1_score_point)
        self.assertEqual(3, match.player2_score_point)

    def test_start_tiebreak(self):
        """Проверка на начало тайбрейка"""
        match = TennisMatch(self.match_in_db)

        # добавление по 5 поинтов в гейме
        for _ in range(5):
            match.add_point_game('player1')
            match.add_point_game('player2')
        self.assertEqual(5, match.player1_score_game)
        self.assertEqual(5, match.player2_score_game)
        self.assertEqual(None, match.tiebreak)

        # добавление по 4 поинта
        for _ in range(4):
            match.add_point({'name': 'player1', 'value': 1})
        self.assertEqual(6, match.player1_score_game)
        for _ in range(4):
            match.add_point({'name': 'player2', 'value': 1})
        self.assertEqual(6, match.player2_score_game)

        self.assertEqual(True, match.tiebreak)

    def test_end_tiebreak(self):
        """Проверка на конец тайбрейка"""
        match = TennisMatch(self.match_in_db)

        # добавление по 6 поинтов в гейме
        for _ in range(5):
            match.add_point_game('player1')
            match.add_point_game('player2')

        # добавление по 5 поинтов
        for _ in range(4):
            match.add_point({'name': 'player1', 'value': 1})
        self.assertEqual(6, match.player1_score_game)
        for _ in range(4):
            match.add_point({'name': 'player2', 'value': 1})
        self.assertEqual(6, match.player2_score_game)

        for _ in range(7):
            match.add_point({'name': 'player1', 'value': 1})

        self.assertEqual(False, match.tiebreak)
        self.assertEqual(1, match.player1_score_set)
        self.assertEqual(0, match.player2_score_set)

    def test_end_match(self):
        """Проверка на окончание матча"""
        match = TennisMatch(self.match_in_db)
        # добавление по 48 поинтов или 2 сетов
        for _ in range(48):
            match.add_point({'name': 'player1', 'value': 1})

        self.assertEqual('player1', match.winner)
