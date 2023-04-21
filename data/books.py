import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Book(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'books'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    genre_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('genres.id'))
    author_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('authors.id'))
    info_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('info.id'))
    image_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('images.id'))
    genre = orm.relationship('Genre')
    author = orm.relationship('Author')
    info = orm.relationship('Info')
    image = orm.relationship('Image')
