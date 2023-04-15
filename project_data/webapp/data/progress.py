import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Progress(SqlAlchemyBase):
    __tablename__ = 'progress'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    end_1 = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    end_2 = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    end_3 = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    user = orm.relationship('User')
