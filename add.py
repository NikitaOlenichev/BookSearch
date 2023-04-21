import requests
import sqlalchemy
from data import db_session
from data.authors import Author
from data.books import Book
from data.genres import Genre
from data.info import Info
from data.images import Image


ats = []
db_session.global_init("db/books.db")
db_sess = db_session.create_session()

for i in range(90, 121):
    res = requests.get(f'https://api.fantlab.ru/work/{i}/extended').json()
    try:
        title = res['work_name']
    except Exception:
        title = '-'
    if title == '-':
        continue
    if not db_sess.query(Book).filter(Book.title == title).first():
        try:
            genre = res['classificatory']['genre_group'][0]['genre'][0]['label']
        except Exception:
            genre = '-'

        try:
            author = res['authors'][0]['name']
        except Exception:
            author = '-'
        try:
            info = res['work_description']
        except Exception:
            info = '-'
        try:
            image = 'https://fantlab.ru' + res['image']
        except Exception:
            image = '-'


        if not db_sess.query(Genre).filter(Genre.title == genre).first():
            db_sess.add(Genre(title=genre))
        if not db_sess.query(Author).filter(Author.name == author).first():
            db_sess.add(Author(name=author))
        if not db_sess.query(Image).filter(Image.link == image).first():
            db_sess.add(Image(link=image))
        if not db_sess.query(Info).filter(Info.info == info).first():
            db_sess.add(Info(info=info))
        db_sess.commit()
        db_sess.add(Book(
            title=title,
            info_id=db_sess.query(Info).filter(Info.info == info).first().id,
            genre_id=db_sess.query(Genre).filter(Genre.title == genre).first().id,
            author_id=db_sess.query(Author).filter(Author.name == author).first().id,
            image_id=db_sess.query(Image).filter(Image.link == image).first().id
        ))
        db_sess.commit()

