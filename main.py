from data import db_session
from flask import Flask, render_template, redirect, request
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
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(
    days=365
)
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
        print(2)
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
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/search/<int:page>', methods=['GET', 'POST'])
def search(page):
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
    print(title_fltr)
    if title_fltr:
        sp = sp.filter(Book.title == title_fltr)
        form.title.data = title_fltr
    if genre_fltr:
        sp = sp.filter(Book.genre == db_sess.query(Genre).filter(Genre.title == genre_fltr).first())
        form.genre.data = genre_fltr
    if author_fltr:
        sp = sp.filter(Book.author == db_sess.query(Author).filter(Author.name == author_fltr).first())
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
                    info.info])
    ln = (len(sp) - 1) // 10 + 1
    pg_f = max(page - 4, 1)
    pg_l = min(page + 4, ln)
    if page < 5:
        pg_l = min(9, ln)
    if page > ln - 4:
        pg_f = max(1, ln - 8)
    return render_template('search.html', title='Поиск', form=form, sp=sp2, page=page, link=f'/search/', ln=len(sp), msg='',
                           author_fltr=author_fltr if author_fltr else '', genre_fltr=genre_fltr if genre_fltr else '', ttl_fltr=title_fltr if title_fltr else '', pg_l=pg_l, pg_f=pg_f)


if __name__ == '__main__':
    db_session.global_init("db/books.db")
    app.run(port=5000, host='127.0.0.1')