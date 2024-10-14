from sqlalchemy.orm import Session


from src.db.create_db_and_tables import MatchesModel
from src.model import Model


class Service:
    def __init__(self, engine):
        self.engine = engine
        self.model = Model(engine)

    def add_point(self, point: dict, data_match: MatchesModel):
        """Добавление очков в матч"""
        data_match.score[point['name']]['points'] += int(point['value'])
        self.model.update_match(data_match)
        return data_match
