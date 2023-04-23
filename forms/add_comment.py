from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class CommentForm(FlaskForm):
    comment_field = TextAreaField('Напишите своё мнение о книге!', validators=[DataRequired()])
    submit = SubmitField('Добавить комментарий')