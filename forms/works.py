import sqlalchemy.orm as orm
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class WorkForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    kind = SelectField('Тип', choices=['Стихотворение', 'Проза'])
    genre = SelectField('Жанр', choices=['эссе', 'эпос', 'эпопея',
                                         'скетч', 'роман', 'рассказ',
                                         'новелла', 'пьеса', 'повесть',
                                         'очерк', 'опус', 'ода'])
    description = TextAreaField("Описание")
    content = TextAreaField("Текст", validators=[DataRequired()])
    submit = SubmitField('Сохранить')

    categories = orm.relation("Category",
                              secondary="association",
                              backref="news")
