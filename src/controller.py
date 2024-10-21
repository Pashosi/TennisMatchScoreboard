from urllib.parse import parse_qs


from src.model import Model


class Controller:

    def new_match(self, environ):
        data_form = self.get_data_form_new_match(environ)
        players = self.names_check(data_form)
        model_obj = Model()
        match = model_obj.add_match(*players)
        request = self.get_match(match.uuid)
        return request

    def names_check(self, data_form: dict):
        """Проверка имен в БД, если нет то добавить"""
        players = []
        for player in data_form:
            name = data_form[player][0]
            model_obj = Model()
            name_player = model_obj.get_player(name)
            if not name_player:
                # model.add_player(name)
                players.append(model_obj.add_player(name))
            else:
                players.append(name_player)
        if len(players) < 2:
            raise Exception('необходимо 2 игрока, а их меньше')
        if players[0] == players[1]:
            raise Exception('игрок не может играть сам с собой')
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

    @staticmethod
    def get_match(uuid):
        """Получение экземпляра матча"""
        model_obj = Model()
        data_match = model_obj.get_match(uuid)
        return data_match

    # def add_point_match(self, environ, data_match):
    #     """Добавление поинта в матч"""
    #     point = self.get_data_match(environ)
    #     service = Service()
    #     request = service.add_point(point, data_match)
    #     return request

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
