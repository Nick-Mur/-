import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    userID = sqlalchemy.Column(sqlalchemy.Integer,
                               index=True, unique=True, nullable=True)
    nickname = sqlalchemy.Column(sqlalchemy.String)
    user_feedback = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    # progress = orm.relationship("Progress", back_populates='user')
