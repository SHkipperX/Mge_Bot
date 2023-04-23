import datetime as dt
import sqlalchemy as sa
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from typing import *


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

    def __repr__(self):
        return f'<{User.__class__.__name__}> {self.id}: {self.user_id}[{self.user_name}]'


class User_Heros(SqlAlchemyBase):
    """
    Перфиксы классов:
    Sn - Sniper; De - Demoman; So - Solder

    Уровни:
    damage - урон; health - здоровье; accuracy - точность
    """
    __tablename__ = 'User_Heros'
    id = sa.Column(sa.Integer, nullable=False, autoincrement=True, primary_key=True)
    user_key = sa.Column(sa.Integer, sa.ForeignKey('Users.id'))

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

