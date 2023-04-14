import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Book(SqlAlchemyBase):
    __tablename__ = 'books'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    genre_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('genres.id'))
    author_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('authors.id'))
    genre = orm.relationship('Genre')
    author = orm.relationship('Author')
    info = sqlalchemy.Column(sqlalchemy.String)