import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Book(SqlAlchemyBase):
    __tablename__ = 'books'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    orig_name = sqlalchemy.Column(sqlalchemy.String)
    genre_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('genres.id'))
    author_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('authors.id'))
    genre = orm.relationship('Genre')
    author = orm.relationship('Author')
    info_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('info.id'))
    image_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('images.id'))
    info = orm.relationship('Info')
    image = orm.relationship('Image')
    work_year = sqlalchemy.Column(sqlalchemy.Integer)
    work_year_of_write = sqlalchemy.Column(sqlalchemy.Integer)
    noms = sqlalchemy.Column(sqlalchemy.String)
    wins = sqlalchemy.Column(sqlalchemy.String)
    similars = sqlalchemy.Column(sqlalchemy.String)
    comments = sqlalchemy.Column(sqlalchemy.String)



