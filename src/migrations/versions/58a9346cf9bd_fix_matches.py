"""fix_matches

Revision ID: 58a9346cf9bd
Revises: 091e076bf989
Create Date: 2024-10-05 20:14:57.228132

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '58a9346cf9bd'
down_revision: Union[str, None] = '091e076bf989'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Players',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('Matches',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('UUID', sa.String(length=255), nullable=False),
    sa.Column('Player1', sa.Integer(), nullable=True),
    sa.Column('Player2', sa.Integer(), nullable=True),
    sa.Column('Winner', sa.Integer(), nullable=True),
    sa.Column('Score', sa.String(length=255), nullable=False),
    sa.ForeignKeyConstraint(['Player1'], ['Players.id'], ),
    sa.ForeignKeyConstraint(['Player2'], ['Players.id'], ),
    sa.ForeignKeyConstraint(['Winner'], ['Players.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('UUID')
    )
    op.drop_index('UUID', table_name='matches')
    op.drop_table('matches')
    op.drop_index('name', table_name='players')
    op.drop_table('players')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('players',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', mysql.VARCHAR(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_index('name', 'players', ['name'], unique=True)
    op.create_table('matches',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('UUID', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('Player1', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('Player2', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('Winner', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('Score', mysql.VARCHAR(length=255), nullable=False),
    sa.ForeignKeyConstraint(['Player1'], ['players.id'], name='matches_ibfk_1'),
    sa.ForeignKeyConstraint(['Player2'], ['players.id'], name='matches_ibfk_2'),
    sa.ForeignKeyConstraint(['Winner'], ['players.id'], name='matches_ibfk_3'),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_index('UUID', 'matches', ['UUID'], unique=True)
    op.drop_table('Matches')
    op.drop_table('Players')
    # ### end Alembic commands ###
