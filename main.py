from data import db_session
from flask import Flask, render_template, redirect, request, make_response, jsonify
from forms.login_form import LoginForm
from forms.register_form import RegisterForm
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from data.users import User
from data.books import Book
from data.authors import Author
from data.info import Info
from data.genres import Genre
from data.images import Image
from forms.search import Search
from forms.add_comment import CommentForm
from flask_restful import Api
from books_resources import BookResource
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(
    days=365
)
api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    db_sess.close()
    return user


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.route('/')
@app.route('/index')
def index():
    if current_user.__class__.__name__ == 'AnonymousUserMixin' or not current_user.image:
        user_image = False
    else:
        user_image = True
    session = db_session.create_session()
    books = session.query(Book).all()
    users = session.query(User).all()
    top_read_list = sorted(books, key=lambda x: x.num_of_readers, reverse=True)[:5]
    top_favorites_list = sorted(books, key=lambda x: x.favorite, reverse=True)[:5]
    top_comments_list = sorted(users, key=lambda x: x.comments, reverse=True)[:5]
    top_read = []
    top_comments = []
    top_favorites = []
    for book in top_read_list:
        top_read.append([book.image.link, book.title, book.id, book.num_of_readers])
    for book in top_favorites_list:
        top_favorites.append([book.image.link, book.title, book.id, book.favorite])
    for user in top_comments_list:
        top_comments.append([user.name, user.comments])
    session.close()
    return render_template('index.html', user_image=user_image, top_read=top_read, top_favorites=top_favorites,
                           top_comments=top_comments)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.username.data).first()
        db_sess.close()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        db_sess.close()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/search/<int:page>', methods=['GET', 'POST'])
def search(page):
    if current_user.__class__.__name__ == 'AnonymousUserMixin' or not current_user.image:
        user_image = False
    else:
        user_image = True
    db_sess = db_session.create_session()
    form = Search()
    sp = db_sess.query(Book)
    if form.validate_on_submit():
        fltr = f'?title={form.title.data}&author={form.author.data}&genre={form.genre.data}'
        return redirect(f'/search/1{fltr}')
    sp2 = []
    author_fltr = request.args.get('author')
    genre_fltr = request.args.get('genre')
    title_fltr = request.args.get('title')
    if title_fltr:
        sp = sp.filter(Book.title.like(f'%{title_fltr}%'))
        form.title.data = title_fltr
    if genre_fltr:
        sp = sp.filter(Book.genre == db_sess.query(Genre).filter(Genre.title.like(f'%{genre_fltr}%')).first())
        form.genre.data = genre_fltr
    if author_fltr:
        sp = sp.filter(Book.author == db_sess.query(Author).filter(Author.name.like(f'%{author_fltr}%')).first())
        form.author.data = author_fltr
    sp = sp.all()
    sp.sort(key=lambda x: x.title)
    for book in sp[10 * (page - 1): 10 * page]:
        author = db_sess.query(Author).filter(Author.id == book.author_id).first()
        image = db_sess.query(Image).filter(Image.id == book.image_id).first()
        info = db_sess.query(Info).filter(Info.id == book.info_id).first()
        genre = db_sess.query(Genre).filter(Genre.id == book.genre_id).first()
        sp2.append([image.link,
                    book.title,
                    author.name,
                    genre.title,
                    info.info,
                    book.id])
    db_sess.close()
    ln = (len(sp) - 1) // 10 + 1
    pg_f = max(page - 4, 1)
    pg_l = min(page + 4, ln)
    if page < 5:
        pg_l = min(9, ln)
    if page > ln - 4:
        pg_f = max(1, ln - 8)
    return render_template('search.html', title='Поиск', form=form, sp=sp2, page=page, link=f'/search/', ln=ln, msg='',
                           author_fltr=author_fltr if author_fltr else '', genre_fltr=genre_fltr if genre_fltr else '',
                           ttl_fltr=title_fltr if title_fltr else '', pg_l=pg_l, pg_f=pg_f, user_image=user_image)


@app.route('/book_page/<int:book_id>', methods=['GET', 'POST'])
def book_page(book_id):
    if current_user.__class__.__name__ == 'AnonymousUserMixin' or not current_user.image:
        user_image = False
    else:
        user_image = True
    session = db_session.create_session()
    book = session.query(Book).filter(Book.id == book_id).first()
    if current_user.__class__.__name__ != 'AnonymousUserMixin':
        user = session.query(User).filter(User.id == current_user.id).first()
        books = user.books
        if books:
            books = list(map(int, books.split(';')[:-1]))
        favorite_books = user.favorite_books
        if favorite_books:
            favorite_books = list(map(int, favorite_books.split(';')[:-1]))
    else:
        user = ''
        books = ''
        favorite_books = ''
    image = book.image.link
    title = book.title
    genre = book.genre.title
    author = book.author.name
    info = book.info.info
    work_year = book.work_year
    work_year_of_write = book.work_year_of_write
    num_of_readers = book.num_of_readers
    favorites = book.favorite
    noms = book.noms
    orig_name = book.orig_name
    if noms:
        noms = noms.split(';')
    wins = book.wins
    if wins:
        wins = wins.split(';')
    similars = book.similars
    if similars:
        similars = similars.split(';')
    comment_form = CommentForm()
    if comment_form.validate_on_submit():
        if not book.comments:
            book.comments = ''
        book.comments += f'{current_user.name}&{comment_form.comment_field.data}&' \
                         f'{datetime.datetime.now().strftime("%H:%M:%S %m.%d.%Y")}#'
        comment_form.comment_field.data = None
        user.comments += 1
        session.commit()
        return redirect(f'/book_page/{book_id}')
    comments = book.comments
    if comments:
        comments = comments.split('#')[:-1]
        comments = list(map(lambda x: x.split('&'), comments))
    session.close()
    return render_template('book_page.html', image=image, title=title, author=author, genre=genre, info=info, noms=noms,
                           similars=similars, wins=wins, work_year_of_write=work_year_of_write, work_year=work_year,
                           form=comment_form, comments=comments, orig_name=orig_name, book_id=book_id,
                           user_books=books if books else [], favorite_books=favorite_books if favorite_books else [],
                           num_of_readers=num_of_readers, favorites=favorites, user_image=user_image)


@app.route('/add_book/<int:book_id>')
def add_book(book_id):
    session = db_session.create_session()
    user = session.query(User).filter(User.id == current_user.id).first()
    book = session.query(Book).filter(Book.id == book_id).first()
    book.num_of_readers += 1
    books = user.books
    if not books:
        books = ''
    books += str(book_id) + ';'
    user.books = books
    session.commit()
    session.close()
    return redirect(f'/book_page/{book_id}')


@app.route('/del_book/<int:book_id>')
def del_book(book_id):
    session = db_session.create_session()
    user = session.query(User).filter(User.id == current_user.id).first()
    book = session.query(Book).filter(Book.id == book_id).first()
    book.num_of_readers -= 1
    books = user.books.split(';')[:-1]
    del books[books.index(str(book_id))]
    if books:
        books = ';'.join(books) + ';'
    else:
        books = ''
    user.books = books
    session.commit()
    session.close()
    return redirect(f'/book_page/{book_id}')


@app.route('/add_favorite_book/<int:book_id>')
def add_favorite_book(book_id):
    session = db_session.create_session()
    user = session.query(User).filter(User.id == current_user.id).first()
    book = session.query(Book).filter(Book.id == book_id).first()
    book.favorite += 1
    books = user.favorite_books
    if not books:
        books = ''
    books += str(book_id) + ';'
    user.favorite_books = books
    session.commit()
    session.close()
    return redirect(f'/book_page/{book_id}')


@app.route('/del_favorite_book/<int:book_id>')
def del_favorite_book(book_id):
    session = db_session.create_session()
    user = session.query(User).filter(User.id == current_user.id).first()
    book = session.query(Book).filter(Book.id == book_id).first()
    book.favorite -= 1
    books = user.favorite_books.split(';')[:-1]
    del books[books.index(str(book_id))]
    if books:
        books = ';'.join(books) + ';'
    else:
        books = None
    user.favorite_books = books
    session.commit()
    session.close()
    return redirect(f'/book_page/{book_id}')


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if current_user.__class__.__name__ == 'AnonymousUserMixin' or not current_user.image:
        user_image = False
    else:
        user_image = True
    session = db_session.create_session()
    user = session.query(User).filter(User.id == current_user.id).first()
    if request.method == 'POST':
        f = request.files['file']
        with open(f'./static/img/users/{current_user.id}.jpg', 'wb') as img:
            img.write(f.read())
        if not user.image:
            user.image = True
        session.commit()
        session.close()
        return redirect('/profile')
    user_id = user.id
    favorites_list = list(map(int, user.favorite_books.split(';')[:-1])) if user.favorite_books else ''
    read_books_list = list(map(int, user.books.split(';')[:-1])) if user.books else ''
    favorites = []
    read_books = []
    for book_id in favorites_list:
        book = session.query(Book).filter(Book.id == book_id).first()
        favorites.append([book.image.link, book.title, book_id])
    for book_id in read_books_list:
        book = session.query(Book).filter(Book.id == book_id).first()
        read_books.append([book.image.link, book.title, book_id])
    cnt_favorite_shelfs = (len(favorites) - 1) // 5 + 1
    cnt_read_shelfs = (len(read_books) - 1) // 5 + 1
    session.close()
    return render_template('profile.html', name=current_user.name, image=user.image, user_id=user_id,
                           favorites=favorites, cnt_favorite_shelfs=cnt_favorite_shelfs,
                           cnt_read_shelfs=cnt_read_shelfs, read_books=read_books, cnt_read_books=len(read_books),
                           cnt_favorites=len(favorites), comments=user.comments, user_image=user_image)


def main():
    db_session.global_init("db/books.db")
    api.add_resource(BookResource, '/api/book/<book_title>')
    app.run(port=5000, host='127.0.0.1')


if __name__ == '__main__':
    main()