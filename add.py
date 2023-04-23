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

for i in range(1, 20):
    res = requests.get(f'https://api.fantlab.ru/work/{i}/extended').json()
    try:
        title = res['work_name']
    except Exception:
        title = '-'
    if title == '-' or not title:
        continue
    orig_title = res['work_name_orig']
    if not db_sess.query(Book).filter(Book.title == title).first():
        try:
            genre = res['classificatory']['genre_group'][0]['genre'][0]['label']
        except Exception:
            genre = '-'

        try:
            authors_req = res['authors']
            authors = ''
            for aut in authors_req:
                if aut['type'] == 'autor':
                    author = aut['name']
                    break
        except Exception:
            author = '-'
        info = res.get('work_description', '-')
        try:
            image = 'https://fantlab.ru' + res['image']
        except Exception:
            image = '-'
        work_year = res.get('work_year', '-')
        work_year_of_write = res.get('work_year_of_write', '-')
        note = res.get('work_notes', '-')
        awards_req = res.get('awards')
        noms = ''
        wins = ''
        if awards_req:
            nom_req = awards_req.get('nom')
            if nom_req:
                for nom in nom_req:
                    noms += f'{nom.get("award_rusname", "-")} ({nom.get("contest_year", "-")});'
            wins_req = awards_req.get('win')
            if wins_req:
                for win in wins_req:
                    wins += f'{win.get("award_rusname", "")} ({win.get("contest_year", "-")});'
        res = requests.get(f'https://api.fantlab.ru/work/{i}/similars').json()
        similars = ''
        for similar in res:
            similars += f'{similar.get("name", "")};'
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
            orig_name=orig_title,
            info_id=db_sess.query(Info).filter(Info.info == info).first().id,
            genre_id=db_sess.query(Genre).filter(Genre.title == genre).first().id,
            author_id=db_sess.query(Author).filter(Author.name == author).first().id,
            image_id=db_sess.query(Image).filter(Image.link == image).first().id,
            similars=similars,
            work_year=work_year,
            work_year_of_write=work_year_of_write,
            noms=noms,
            wins=wins,
        ))
        db_sess.commit()

