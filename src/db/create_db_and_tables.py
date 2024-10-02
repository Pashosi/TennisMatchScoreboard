import sqlalchemy as sa
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

players = sa.Table(
    'Players', meta,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('name', sa.VARCHAR(255), nullable=False, unique=True)
)

matches = sa.Table(
    'Matches', meta,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('UUID', sa.String(255), nullable=False, unique=True),
    sa.Column('Player1', sa.Integer, sa.ForeignKey('Players.id')),
    sa.Column('Player2', sa.Integer, sa.ForeignKey('Players.id')),
    sa.Column('Winner', sa.Integer, sa.ForeignKey('Players.id')))

engine = sa.create_engine(f'mysql+mysqlconnector://root:root@localhost:3306/{db_config["mysql"]["name"]}', echo=True)

meta.create_all(engine)

