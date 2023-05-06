import datetime as dt
import sqlalchemy as sa
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from typing import *

"""
Перфиксы классов:
sn - Sniper; de - Demoman; so - Solder

Уровни:
damage - урон; health - здоровье; accuracy - точность

class User - основные данные пользователя
class User_Heros - данные о уровне персонажей
class User_Stat - Статистика о каждом персонаже: урон, выстрелы, попадания, игры, победы, поражения
"""


class User(SqlAlchemyBase):
    __tablename__ = 'Users'

    id = sa.Column(sa.Integer, nullable=False, autoincrement=True, primary_key=True)
    user_id = sa.Column(sa.Integer, nullable=False, unique=True)
    user_name = sa.Column(sa.String, nullable=False)
    reg_date = sa.Column(sa.DateTime, nullable=False, default=dt.datetime.now())

    points = sa.Column(sa.Integer, nullable=False, default=0)
    count_of_game = sa.Column(sa.Integer, nullable=False, default=0)
    wins = sa.Column(sa.Integer, nullable=False, default=0)
    loses = sa.Column(sa.Integer, nullable=False, default=0)

    heros = orm.relationship('User_Heros', back_populates='user')
    stats = orm.relationship('User_Stat', back_populates='user')

    def __repr__(self):
        return f'<{User.__class__.__name__}> {self.id}: {self.user_id}[{self.user_name}]'


class User_Heros(SqlAlchemyBase):
    __tablename__ = 'User_Heros'
    id = sa.Column(sa.Integer, nullable=False, autoincrement=True, primary_key=True)
    user_key = sa.Column(sa.Integer, sa.ForeignKey('Users.id'))
    credits = sa.Column(sa.Integer, nullable=False, default=0)

    sn_damage = sa.Column(sa.Integer, nullable=False, default=1)
    sn_health = sa.Column(sa.Integer, nullable=False, default=1)
    sn_accuracy = sa.Column(sa.Integer, nullable=False, default=1)

    de_damage = sa.Column(sa.Integer, nullable=False, default=1)
    de_health = sa.Column(sa.Integer, nullable=False, default=1)
    de_accuracy = sa.Column(sa.Integer, nullable=False, default=1)

    so_damage = sa.Column(sa.Integer, nullable=False, default=1)
    so_health = sa.Column(sa.Integer, nullable=False, default=1)
    so_accuracy = sa.Column(sa.Integer, nullable=False, default=1)

    user = orm.relationship('User')

    def __repr__(self):
        print(f'<{User_Heros.__class__.__name__}> ({self.id})<-Key={self.user_key}')


class User_Stat(SqlAlchemyBase):
    __tablename__ = 'users_stat'
    id = sa.Column(sa.Integer, nullable=False, autoincrement=True, primary_key=True)
    user_key = sa.Column(sa.Integer, sa.ForeignKey('Users.id'))

    sn_damage = sa.Column(sa.Integer, nullable=False, default=0)
    sn_shot = sa.Column(sa.Integer, nullable=False, default=0)
    sn_hits = sa.Column(sa.Integer, nullable=False, default=0)
    sn_games = sa.Column(sa.Integer, nullable=False, default=0)
    sn_wins = sa.Column(sa.Integer, nullable=False, default=0)
    sn_loses = sa.Column(sa.Integer, nullable=False, default=0)

    so_damage = sa.Column(sa.Integer, nullable=False, default=0)
    so_shot = sa.Column(sa.Integer, nullable=False, default=0)
    so_hits = sa.Column(sa.Integer, nullable=False, default=0)
    so_games = sa.Column(sa.Integer, nullable=False, default=0)
    so_wins = sa.Column(sa.Integer, nullable=False, default=0)
    so_loses = sa.Column(sa.Integer, nullable=False, default=0)

    de_damage = sa.Column(sa.Integer, nullable=False, default=0)
    de_shot = sa.Column(sa.Integer, nullable=False, default=0)
    de_hits = sa.Column(sa.Integer, nullable=False, default=0)
    de_games = sa.Column(sa.Integer, nullable=False, default=0)
    de_wins = sa.Column(sa.Integer, nullable=False, default=0)
    de_loses = sa.Column(sa.Integer, nullable=False, default=0)

    user = orm.relationship('User')

    def __repr__(self):
        print(f'<{User_Stat.__class__.__name__}> ({self.id})<-Key={self.user_key}')