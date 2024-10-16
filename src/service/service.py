from sqlalchemy.orm import Session


from src.db.create_db_and_tables import MatchesModel
from src.model import Model


class Service:

    def add_point(self, point: dict, data_match: MatchesModel):
        """Добавление очков в матч"""
        data_match.score[point['name']]['points'] += int(point['value'])
        model_obj = Model()
        model_obj.update_match(data_match)
        return data_match
