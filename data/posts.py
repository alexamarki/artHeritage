import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Posts(SqlAlchemyBase):
    __tablename__ = 'posts'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    content_id = sqlalchemy.Column(sqlalchemy.Integer,
                             sqlalchemy.ForeignKey("content.id"), nullable=True, default=None)
    is_public = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
    u_title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    u_content = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    u_id = sqlalchemy.Column(sqlalchemy.Integer,
                             sqlalchemy.ForeignKey("users.id"))
    post_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    users = orm.relationship('Users')
    content = orm.relationship('Content')