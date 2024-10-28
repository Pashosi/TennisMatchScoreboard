from src.controller import Controller
import random
from src.service.tennis_match import TennisMatch

tennis_players = [
    "Federer",
    "Nadal",
    "Djokovic",
    "Sampras",
    "Agassi",
    "Borg",
    "Lendl",
    "Connors",
    "McEnroe",
    "Smith",
    "Laver",
    "Murray",
    "Hewitt",
    "Rios",
    "Berdych",
    "Muster",
    "Moya",
    "Zverev",
    "Tsitsipas",
    "Medvedev"
]

controller = Controller()

for i in range(20):
    name1 = random.choice(tennis_players)
    name2 = random.choice(tennis_players)
    while name1 == name2:
        name1 = random.choice(tennis_players)
        name2 = random.choice(tennis_players)

    input_names = {'name1':[random.choice(tennis_players)], 'name2':[random.choice(tennis_players)]}
    data_form = controller.new_match(test_data=input_names) # создаем матч и получаем его экземпляр
    match = TennisMatch(data_form)
    while not match.winner:  # добавляем поинты пока не определили победителя
        match.add_point({'name': 'player1', 'value': 1})
    if match.winner:
        match.update_match_in_bd()