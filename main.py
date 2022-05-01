from flask import *
from flask import jsonify
from flask_login import (LoginManager, login_user,
                         logout_user, login_required, current_user)
from forms.user import RegisterForm, LoginForm
from forms.works import WorkForm
from sqlalchemy.orm import joinedload
from sqlalchemy.sql.expression import desc
from requests import get, post, delete


from data.works import Works
from data.users import User
from data.kind import Kind
from data.genre import Genre
from data import db_session, works_api
from flask_restful import reqparse, abort, Api, Resource
# from data.news_resources import *

KINDS = ['Стихотворение', 'Проза']
GENRES = ['эссе', 'эпос', 'эпопея',
          'скетч', 'роман', 'рассказ',
          'новелла', 'пьеса', 'повесть',
          'очерк', 'опус', 'ода']

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


def main():
    db_session.global_init("db/poems.db")
    app.register_blueprint(works_api.blueprint)

    _insert_data()
    app.run()


def _insert_data():
    db_sess = db_session.create_session()

    if not db_sess.query(Kind).all():
        for idx, name in enumerate(KINDS):
            poem = Kind(
                id=idx + 1,
                name=name,
            )
            db_sess.add(poem)
    if not db_sess.query(Genre).all():
        for idx, name in enumerate(GENRES):
            poem = Genre(
                id=idx + 1,
                name=name,
            )
            db_sess.add(poem)

    db_sess.commit()


@app.route("/")
def index():
    db_sess = db_session.create_session()
    works = db_sess.query(Works).order_by(
        desc(Works.created_date))
    return render_template("index.html", works=works)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(
            User.email == form.email.data).first()
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
        login_user(user, remember=True)
        return redirect('/')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/logout')
def logout():
    logout_user()

    return redirect("/")


@app.route('/profile/<int:user_id>')
def profile(user_id):
    db_sess = db_session.create_session()
    works = db_sess.query(Works).order_by(
        desc(Works.created_date)).filter(Works.user_id == user_id)
    return render_template('profile.html', user=load_user(user_id), works=works)


@app.route("/add_work", methods=['GET', 'POST'])
def add_work():
    form = WorkForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        work = Works(
            title=form.title.data,
            kind_id=KINDS.index(form.kind.data) + 1,
            genre_id=GENRES.index(form.genre.data) + 1,
            content=form.content.data,
            description=form.description.data,
            is_private=False,
            user_id=current_user.id
        )
        db_sess.add(work)
        db_sess.commit()

        return redirect(f'/profile/{current_user.id}')

    return render_template('works.html', form=form)


@app.route('/texts/<int:work_id>')
def get_work(work_id):
    db_sess = db_session.create_session()
    work = db_sess.query(Works).get(work_id)

    # work.content = work.content.replace('', '')
    work.content = work.content.split('\r\n')
    a = [work.content]
    print(a)
    return render_template('text.html', work=work)
    return work.to_dict(only=(
        'title', 'kind.name', 'genre.name',
        'description', 'content', 'user_id', 'is_private'))

@app.route("/test/<int:n>")
def test_func(n):
    # return get(f'http://localhost:5000/api/works/newest/{n}').json()
    print(current_user)
    return 'asd'


if __name__ == '__main__':
    main()
