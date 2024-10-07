import sqlalchemy as sa
from sqlalchemy.orm import as_declarative, Mapped, mapped_column, Session

from src.config import db_config
from mysql.connector import Error, connect

# try:
#     with connect(
#         host=db_config["mysql"]["host"],
#         user=db_config["mysql"]["user"],
#         password=db_config["mysql"]["password"],
#     ) as connection:
#         create_db_query = 'CREATE DATABASE IF NOT EXISTS tennis_match_db'
#         with connection.cursor() as cursor:
#             cursor.execute(create_db_query)
# except Error as e:
#     print(e)


meta = sa.MetaData()
#
# players = sa.Table(
#     'Players', meta,
#     sa.Column('id', sa.Integer, primary_key=True),
#     sa.Column('name', sa.VARCHAR(255), nullable=False, unique=True)
# )
#
# matches = sa.Table(
#     'Matches', meta,
#     sa.Column('id', sa.Integer, primary_key=True),
#     sa.Column('UUID', sa.String(255), nullable=False, unique=True),
#     sa.Column('Player1', sa.Integer, sa.ForeignKey('Players.id')),
#     sa.Column('Player2', sa.Integer, sa.ForeignKey('Players.id')),
#     sa.Column('Winner', sa.Integer, sa.ForeignKey('Players.id')),
#     sa.Column('Score', sa.String(255), nullable=False))
#
engine = sa.create_engine(f'mysql+mysqlconnector://root:root@localhost:3306/{db_config["mysql"]["name"]}', echo=True)
#
# meta.create_all(engine)
@as_declarative(metadata=meta)
class AbstractModel:
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)


class PlayersModel(AbstractModel):
    __tablename__ = 'Players'

    name: Mapped[str] = mapped_column(sa.VARCHAR(255), nullable=False, unique=True)

class MatchesModel(AbstractModel):
    __tablename__ = 'Matches'

    UUID: Mapped[str] = mapped_column(nullable=False, unique=True)
    Player1: Mapped[int] = mapped_column(sa.ForeignKey('Players.id'))
    Player2: Mapped[int] = mapped_column(sa.ForeignKey('Players.id'))
    Winner: Mapped[int] = mapped_column(sa.ForeignKey('Players.id'))
    Score: Mapped[str] = mapped_column(nullable=False)


# with Session(engine) as session:
#     with session.begin():
#         AbstractModel.metadata.create_all(engine)
# with Session(engine) as session:
#     with session.begin():
#         user = PlayersModel(name='Nadal')   # noqa
#         session.add(user)
