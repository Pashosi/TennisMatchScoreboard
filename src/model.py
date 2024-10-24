from uuid import uuid4

import sqlalchemy as sa
from sqlalchemy.orm import Session, joinedload

from src.db.create_db_and_tables import PlayersModel, MatchesModel, engine


class Model:

    def get_player(self, player):
        with Session(engine) as session:
            res = session.execute(sa.select(PlayersModel).where(PlayersModel.name == player))
            n = res.scalar()
            if n:
                print(n)

                return n
            print('игрок не найден')
            return []

    def add_player(self, name):
        """Добавление игрока в БД и возвращение его экземпляра"""
        with Session(engine) as session:
            with session.begin():
                session.add(PlayersModel(name=name))  # noqa
                print(f'вставлен новый игрок {name}')
                player = session.execute(sa.select(PlayersModel).where(PlayersModel.name == name))

            return player.scalar()

    def add_match(self, player1, player2):
        with Session(engine) as session:
            match = MatchesModel(
                player1=player1,
                player2=player2,
                uuid=str(uuid4()),
                score={
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
                },
            )
            session.add(match)
            session.commit()
            return session.execute(sa.select(MatchesModel).where(MatchesModel.id == match.id)).scalar()

    def get_match(self, uuid):
        with Session(engine) as session:
            request = (
                session.execute(
                    sa.select(MatchesModel)
                    .options(joinedload(MatchesModel.player1),
                             joinedload(MatchesModel.player2),
                             joinedload(MatchesModel.winner))  # загружаем связанные объекты
                    .where(MatchesModel.uuid == uuid)
                )
                .scalar()
            )
            return request

    def update_winner_and_score_match(self, uuid, name_winner: PlayersModel, data: dict):
        with Session(engine) as session:
            # obj = session.query(MatchesModel).filter(MatchesModel.uuid == uuid).first()
            # obj.score = data
            # obj.winner_fk = self.get_player(name_winner.name).id
            # session.commit()
            session.execute(
                sa.update(MatchesModel).where(MatchesModel.uuid == uuid).values(score=data, winner_fk=name_winner.id)
            )

            session.commit()
