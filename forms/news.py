import sqlalchemy.orm as orm
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class WorkForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    content = TextAreaField("Текст")
    a = SelectField('as', choices=[('cpp', 'C++'), ('py', 'Python'), ('text', 'Plain Text')])
    submit = SubmitField('Применить')

    categories = orm.relation("Category",
                          secondary="association",
                          backref="news")
