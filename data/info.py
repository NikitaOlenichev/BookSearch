import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Info(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'info'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    info = sqlalchemy.Column(sqlalchemy.String, nullable=True)