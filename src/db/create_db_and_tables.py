import os
from uuid import UUID
from dotenv import load_dotenv
import sqlalchemy as sa
from mysql.connector import Error, connect

from sqlalchemy.dialects.mysql import JSON
from sqlalchemy.orm import as_declarative, Mapped, mapped_column, relationship

from config import db_config

load_dotenv()
NAME = os.getenv('NAME')
PASSWORD = os.getenv('PASSWORD')

try:
    with connect(
        host=db_config["mysql"]["host"],
        user=NAME,
        password=PASSWORD,
    ) as connection:
        create_db_query = 'CREATE DATABASE IF NOT EXISTS tennis_match_db'
        with connection.cursor() as cursor:
            cursor.execute(create_db_query)
except Error as e:
    print(e)

engine = sa.create_engine(f'mysql+mysqlconnector://{NAME}:{PASSWORD}@localhost:3306/{db_config["mysql"]["name"]}', echo=True)

meta = sa.MetaData()


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

    uuid: Mapped[UUID] = mapped_column(sa.String(255), nullable=False, unique=True)
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
