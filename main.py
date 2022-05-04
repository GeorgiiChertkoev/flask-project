import datetime

from flask import *
from flask import jsonify
from flask_login import (LoginManager, login_user,
                         logout_user, login_required,
                         current_user)
from forms.user import RegisterForm, LoginForm
from forms.works import WorkForm
from sqlalchemy.orm import joinedload
import sqlalchemy
from sqlalchemy.sql.expression import desc
from requests import get, post, delete


from data.works import Works
from data.users import User
from data.genre import Genre
from data import db_session, works_api
from flask_restful import reqparse, abort, Api
# from data.news_resources import *

GENRES = ['эссе', 'эпос', 'эпопея',
          'скетч', 'роман', 'рассказ',
          'новелла', 'пьеса', 'повесть',
          'очерк', 'сказка', 'ода']

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
    return render_template("index.html",
                           headline='Последние работы',
                           works=works)


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
    return render_template('login.html',
                           title='Авторизация',
                           form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html',
                                   title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html',
                                   title='Регистрация',
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
    return render_template('register.html',
                           title='Регистрация',
                           form=form)


@app.route('/logout')
def logout():
    logout_user()

    return redirect("/")


@app.route('/profile/<int:user_id>')
def profile(user_id):
    """
    Страница профиля
    """
    # print(dir(request))
    # print(request.referrer)

    db_sess = db_session.create_session()
    works = db_sess.query(Works).order_by(
        desc(Works.created_date)).filter(Works.user_id == user_id).all()
    # print(works.all())
    # print(len(works.all()))
    return render_template('profile.html',
                           user=load_user(user_id),
                           works=works)


@app.route("/add_work", methods=['GET', 'POST'])
def add_work():
    """
    Добавление работы по форме
    """
    form = WorkForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        work = Works(
            title=form.title.data,
            genre_id=GENRES.index(form.genre.data) + 1,
            content=form.content.data,
            description=form.description.data,
            is_private=False,
            user_id=current_user.id,
            created_date=datetime.datetime.now()
        )
        db_sess.add(work)
        db_sess.commit()

        return redirect(f'/profile/{current_user.id}')

    return render_template('works.html', form=form)


@app.route('/delete_work/<int:work_id>')
def delete_work(work_id):
    db_sess = db_session.create_session()
    work = db_sess.query(Works).get(work_id)

    if not work or work.user_id != int(current_user.get_id()):
        return redirect('/')

    # print(dir(request))
    db_sess.delete(work)
    db_sess.commit()
    return redirect(f'/profile/{current_user.id}')


@app.route('/reduct_work/<int:work_id>', methods=['GET', 'POST'])
def reduct_work(work_id):
    form = WorkForm()

    if request.method == "GET":
        db_sess = db_session.create_session()
        work = db_sess.query(Works).get(work_id)

        # Вставляем имеющиеся данные
        form.title.data = work.title
        form.genre.data = work.genre.name
        form.description.data = work.description
        form.content.data = work.content

    if form.validate_on_submit():
        db_sess = db_session.create_session()
        work = db_sess.query(Works).get(work_id)

        if work:
            # Меняем данные
            work.title = form.title.data
            work.genre_id = GENRES.index(form.genre.data) + 1
            work.content = form.content.data
            work.description = form.description.data

            # нужен из-за того что я отключил "autoflush"
            db_sess.flush()

            db_sess.commit()

            return redirect(f'/profile/{current_user.id}')
        else:
            abort(404)

    return render_template('works.html', form=form)


@app.route('/texts/<int:work_id>')
def get_work(work_id):
    # print(request.referrer)
    db_sess = db_session.create_session()
    work = db_sess.query(Works).get(work_id)
    # work.content = work.content.replace('', '')
    work.content = work.content.split('\r\n')

    return render_template('text.html', work=work)


@app.route('/filtered_by_genre/<int:genre_id>')
def filtered_by_genre(genre_id):
    db_sess = db_session.create_session()
    works = db_sess.query(Works).filter(Works.genre_id == genre_id).order_by(
        desc(Works.created_date))
    return render_template('index.html',
                           headline=f'Работы в жанре {GENRES[genre_id - 1]}',
                           works=works)

@app.errorhandler(404)
def not_found(error):
    return """
        <h1>
        Ошибка 404<br>
        К сожалению, данная страница не существует (っ °Д °;)っ
        </h1>
        <a href="/">
            Перейти на главную
        </a>
    """



@app.route("/test/<int:n>")
def test_func(n):
    # return get(f'http://localhost:5000/api/works/newest/{n}').json()
    print(current_user)
    return 'asd'


if __name__ == '__main__':
    main()
