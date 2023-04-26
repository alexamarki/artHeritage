import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Content(SqlAlchemyBase):
    __tablename__ = 'content'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    content_src = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    content_img = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    content_title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    content_creator = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    content_date = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    interactions = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    latest_interaction = sqlalchemy.Column(sqlalchemy.DateTime,
                                           default=datetime.datetime.now)
    bookmarks = orm.relationship("Bookmarks", back_populates="content")
    posts = orm.relationship("Posts", back_populates="content")
