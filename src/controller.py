from urllib.parse import parse_qs

from src.db.create_db_and_tables import engine
from src.model import Model
from src.service import Service

# model = Model(engine)
# service = Service(engine)

class Controller:
    def __init__(self):
        self.model = Model(engine)
        self.service = Service(engine)

    def new_match(self, environ):
        data_form = self.get_data_form_new_match(environ)
        players = self.names_check(data_form)
        request = self.model.add_match(*players)

        return request

    def names_check(self, data_form: dict):
        """Проверка имен в БД, если нет то добавить"""
        players = []
        for player in data_form:
            name = data_form[player][0]
            name_player = self.model.get_player(name)
            if not name_player:
                # model.add_player(name)
                players.append(self.model.add_player(name))
            else:
                players.append(name_player)
        return players

    def get_data_form_new_match(self, environ):
        """Получение данных из формы нового матча"""
        response_body = int(environ.get('CONTENT_LENGTH', 0))
        body = environ['wsgi.input'].read(response_body).decode('utf-8')
        post_data = parse_qs(body)

        # Извлекаем данные формы (имя и сообщение)
        name1 = post_data.get('name1', [''])[0]
        name2 = post_data.get('name2', [''])[0]
        print(name1, name2, sep=': ')
        # post_data = {'name1': ['wada'], 'name2': ['adaw']}
        return post_data

    def get_match_score(self, uuid):
        """Полчение экземпляра матча"""
        data_match = self.model.get_match(uuid)
        return data_match

    def add_point_match(self, environ, data_match):
        """Добавление поинта в матч"""
        point = self.get_data_match(environ)
        request = self.service.add_point(point, data_match)
        return request

    def get_data_match(self, environ):
        """Получение данных из кнопки матча"""
        response_body = int(environ.get('CONTENT_LENGTH', 0))
        body = environ['wsgi.input'].read(response_body).decode('utf-8')
        post_data = parse_qs(body)

        # Извлекаем данные формы (имя и сообщение)
        n = 1
        name = next(iter(post_data))
        value = post_data[name][0]
        return {'name': name, 'value': value}
