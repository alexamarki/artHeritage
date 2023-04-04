import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Bookmarks(SqlAlchemyBase):
    __tablename__ = 'bookmarks'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    content_src = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    content_img = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    content_title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    is_public = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
    u_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    book_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    users = orm.relationship('Users')