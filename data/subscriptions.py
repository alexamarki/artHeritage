import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Subscriptions(SqlAlchemyBase):
    __tablename__ = 'subscriptions'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    u_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    u_follower_id = sqlalchemy.Column(sqlalchemy.Integer)
    users = orm.relationship('Users')
