import sqlalchemy as sa
from sqlalchemy.orm import Session

from src.db.create_db_and_tables import PlayersModel


class Model:
    def __init__(self, engine):
        self.engine = engine

    def get_player(self, name):
        with Session(self.engine) as session:
            with session.begin():
                res = session.execute(sa.select(PlayersModel).where(PlayersModel.name == name))
                if res.scalar():
                    return res
                print('игрок не найден')
                return []

    def add_player(self, name):
        with Session(self.engine) as session:
            with session.begin():
                session.add(PlayersModel(name=name))  # noqa
                print(f'вставлен новый игрок {name}')
