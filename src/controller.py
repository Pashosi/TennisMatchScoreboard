from urllib.parse import parse_qs

from src.db.create_db_and_tables import engine
from src.model import Model

model = Model(engine)


class Controller:

    def new_match(self, environ):
        data_form = self.get_data_form_new_match(environ)
        players = self.names_check(data_form)
        request = model.add_match(*players)

        return request

    def names_check(self, data_form: dict):
        """Проверка имен в БД, если нет то добавить"""
        players = []
        for player in data_form:
            name = data_form[player][0]
            name_player = model.get_player(name)
            if not name_player:
                # model.add_player(name)
                players.append(model.add_player(name))
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

    def get_data_match_score(self, uuid):
        """Полчение данных о матче"""
        data_match = model.get_match(uuid)
        return data_match
