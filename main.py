from flask import *
from flask import jsonify
from flask_login import (LoginManager, login_user,
                         logout_user, login_required, current_user)
# from forms.user import RegisterForm, LoginForm
# from forms.news import NewsForm
from sqlalchemy.orm import joinedload
from sqlalchemy.sql.expression import desc

from requests import get, post, delete


from data.works import Works
from data.users import User
from data import db_session, works_api
from flask_restful import reqparse, abort, Api, Resource
# from data.news_resources import *


app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
# login_manager = LoginManager()
# login_manager.init_app(app)


def main():
    db_session.global_init("db/poems.db")
    app.register_blueprint(works_api.blueprint)
    # db_sess = db_session.create_session()

    # for a in db_sess.query(Works).options(joinedload("genre")):
    #     pass
    #     # print(a.genre.name)
    # for a in db_sess.query(Works).order_by(desc(Works.created_date)).limit(2):
    #     print(a.content, a.genre.name)

    app.run()


@app.route("/")
def index():
    db_sess = db_session.create_session()
    works = db_sess.query(Works).order_by(desc(Works.created_date)).limit(3)
    # print(works[0].title)
    # if current_user.is_authenticated:
    #     news = db_sess.query(News).filter(
    #         (News.user == current_user) | (News.is_private != True))
    # else:
    #     news = db_sess.query(News).filter(News.is_private != True)
    return render_template("index.html", works=works)


@app.route("/test/<int:n>")
def test_func(n):
    return get(f'http://localhost:5000/api/works/newest/{n}').json()


if __name__ == '__main__':
    main()
    

# print(get('http://127.0.0.1:5000/api/works/newest/2'))
