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
            session.execute(
                sa.update(MatchesModel).where(MatchesModel.uuid == uuid).values(score=data, winner_fk=name_winner.id)
            )

            session.commit()

    def get_matches(self, start_id=None, end_id=None, filter=None):
        with Session(engine) as session:

            if start_id and end_id:
                return session.execute(sa.select(MatchesModel).order_by(MatchesModel.id).options(
                    joinedload(MatchesModel.player1),
                    joinedload(MatchesModel.player2),
                    joinedload(MatchesModel.winner)).where(MatchesModel.id.between(start_id, end_id)).where(
                    MatchesModel.winner_fk != None)).scalars().all()
            if start_id:
                return session.execute(sa.select(MatchesModel).order_by(MatchesModel.id).options(
                    joinedload(MatchesModel.player1),
                    joinedload(MatchesModel.player2),
                    joinedload(MatchesModel.winner)).where(MatchesModel.id >= start_id).where(
                    MatchesModel.winner_fk != None)).scalars().all()
            if end_id:
                return session.execute(sa.select(MatchesModel).order_by(MatchesModel.id).options(
                    joinedload(MatchesModel.player1),
                    joinedload(MatchesModel.player2),
                    joinedload(MatchesModel.winner)).where(MatchesModel.id <= end_id).where(
                    MatchesModel.winner_fk != None)).scalars().all()
            if filter:
                return session.execute(sa.select(MatchesModel).order_by(MatchesModel.id).options(
                    joinedload(MatchesModel.player1),
                    joinedload(MatchesModel.player2),
                    joinedload(MatchesModel.winner)).where(
                    MatchesModel.winner_fk == filter).where(MatchesModel.winner_fk != None)).scalars().all()

            return session.execute(sa.select(MatchesModel).order_by(MatchesModel.id).options(
                joinedload(MatchesModel.player1),
                joinedload(MatchesModel.player2),
                joinedload(MatchesModel.winner)).where(
                MatchesModel.winner_fk != None)).scalars().all()

    def get_players_winner_matches(self):
        with Session(engine) as session:
            return session.execute(
                sa.select(PlayersModel.name).select_from(MatchesModel)
                .join(PlayersModel, PlayersModel.id == MatchesModel.winner_fk)
                .where(MatchesModel.winner_fk.isnot(None))
            ).scalars().all()
