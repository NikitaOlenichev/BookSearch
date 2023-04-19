from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, SelectField
from wtforms.validators import DataRequired


class Search(FlaskForm):
    title = StringField('Название')
    author = StringField('Автор')
    genre = StringField('Жанр')
    submit = SubmitField('Поиск')
