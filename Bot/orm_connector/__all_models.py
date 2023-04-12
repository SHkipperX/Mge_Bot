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

    def __repr__(self):
        return f'{User.__class__.__name__} {self.id}: {self.user_id}[{self.user_name}]'
