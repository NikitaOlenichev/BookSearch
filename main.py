import books_resources
from data import db_session
from flask import Flask, render_template, redirect
from forms.login_form import LoginForm
from forms.register_form import RegisterForm
from flask_login import LoginManager, login_user, logout_user, login_required
from data.users import User
from data.books import Book
from data.authors import Author
from data.info import Info
from data.genres import Genre
from data.images import Image
from forms.search import Search
from flask_restful import reqparse, abort, Api, Resource
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(
    days=365
)
api = Api(app)
api.add_resource(books_resources.BookResource, '/api/book/<string:book_title>')
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
    return db_sess.query(User).get(user_id)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    print(form.username)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
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
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/search/<int:page>', methods=['GET', 'POST'])
def search(page):
    db_sess = db_session.create_session()
    sp = db_sess.query(Book).filter(Book.id < 11).all()
    sp2 = []
    for book in sp:
        author = db_sess.query(Author).filter(Author.id == book.author_id).first()
        image = db_sess.query(Image).filter(Image.id == book.image).first()
        info = db_sess.query(Info).filter(Info.id == book.info).first()
        genre = db_sess.query(Genre).filter(Genre.id == book.genre_id).first()
        sp2.append([image.link,
                    book.title,
                    author.name,
                    genre.title,
                    info.info])
    print(sp2)
    form = Search()
    return render_template('search.html', title='Поиск', form=form, sp=sp2)


if __name__ == '__main__':
    db_session.global_init("db/books.db")
    app.run(port=5000, host='127.0.0.1')