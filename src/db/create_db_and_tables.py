from uuid import uuid4, UUID

import sqlalchemy as sa
import uuid as uuid

from sqlalchemy.dialects.mysql import JSON
from sqlalchemy.orm import as_declarative, Mapped, mapped_column, Session, relationship

from src.config import db_config
from mysql.connector import Error, connect

engine = sa.create_engine(f'mysql+mysqlconnector://root:root@localhost:3306/{db_config["mysql"]["name"]}', echo=True)

meta = sa.MetaData()


#
@as_declarative(metadata=meta)
class AbstractModel:
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)


class PlayersModel(AbstractModel):
    __tablename__ = 'players'

    name: Mapped[str] = mapped_column(sa.VARCHAR(255), nullable=False, unique=True, index=True)

    def __repr__(self):
        return f'player: (id={self.id}, name={self.name})'


class MatchesModel(AbstractModel):
    __tablename__ = 'matches'

    uuid: Mapped[UUID] = mapped_column(sa.String(255), default=uuid4().hex, nullable=False, unique=True)
    player1_fk: Mapped[int] = mapped_column(sa.ForeignKey('players.id', ondelete="CASCADE"), nullable=False)
    player2_fk: Mapped[int] = mapped_column(sa.ForeignKey('players.id', ondelete="CASCADE"), nullable=False)
    winner_fk: Mapped[int] = mapped_column(sa.ForeignKey('players.id', ondelete="CASCADE"), nullable=True)
    score: Mapped[JSON] = mapped_column(JSON)

    player1: Mapped["PlayersModel"] = relationship(foreign_keys="MatchesModel.player1_fk")
    player2: Mapped["PlayersModel"] = relationship(foreign_keys="MatchesModel.player2_fk")
    winner: Mapped["PlayersModel"] = relationship(foreign_keys="MatchesModel.winner_fk")

    def __repr__(self):
        return f'match: (id={self.id}, ' \
               f'uuid={self.uuid}, ' \
               f'player1={self.player1}, ' \
               f'player2={self.player2}, ' \
               f'winner={self.winner}, ' \
               f'score={self.score})'


# with Session(engine) as session:
#     with session.begin():
#         AbstractModel.metadata.create_all(engine)

# with Session(engine) as session:
#     with session.begin():
#         player_match1 = session.get(PlayersModel, 5)
#         player_match2 = session.get(PlayersModel, 6)
#
#         # print(player_match1, player_match2)
#         match = MatchesModel(
#             player1=player_match1,
#             player2=player_match2,
#             winner=player_match1,
#             score={'player1': 0, 'player2': 2},
#         )
#         session.add(match)
#         print(player_match1)
#         print(player_match2)