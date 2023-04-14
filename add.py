import requests
import sqlalchemy
from data import db_session
from data.authors import Author
from data.books import Book
from data.genres import Genre


ats = []
db_session.global_init("db/books.db")
db_sess = db_session.create_session()
for i in range(1, 11):
    res = requests.get(f'https://api.fantlab.ru/work/{i}').json()
    genre = res.get('work_type', '-')
    author = res.get('authors', [{'name': '-'}])[0]['name']
    title = res.get('work_name', 0)
    info = res.get('work_description')
    db_sess.add(Genre(title=genre))
    db_sess.add(Author(name=author))
    db_sess.commit()
    db_sess.add(Book(
        title=title,
        info=info,
        genre_id=db_sess.query(Genre).filter(Genre.title == genre).first().id,
        author_id=db_sess.query(Author).filter(Author.name == author).first().id
    ))
    db_sess.commit()