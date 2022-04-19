from flask import *
from flask import jsonify
from flask_login import (LoginManager, login_user,
                         logout_user, login_required, current_user)
# from forms.user import RegisterForm, LoginForm
# from forms.news import NewsForm
from data.works import Works
from data.users import User
# from data import db_session, news_api
from data import db_session
from flask_restful import reqparse, abort, Api, Resource
# from data.news_resources import *


app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
# login_manager = LoginManager()
# login_manager.init_app(app)



def main():
    db_session.global_init("db/poems.db")
    # app.register_blueprint(news_api.blueprint)
    app.run()



@app.route("/")
def index():
    db_sess = db_session.create_session()
    works = db_sess.query(Works).all()
    # print(works[0].title)
    # if current_user.is_authenticated:
    #     news = db_sess.query(News).filter(
    #         (News.user == current_user) | (News.is_private != True))
    # else:
    #     news = db_sess.query(News).filter(News.is_private != True)
    return render_template("index.html", works=works)
    # return works[0].content




# @login_manager.user_loader
# def load_user(user_id):
#     db_sess = db_session.create_session()
#     return db_sess.query(User).get(user_id)


if __name__ == '__main__':
    # api.add_resource(NewsListResource, '/api/v2/news') 
    # api.add_resource(NewsResource, '/api/v2/news/<int:news_id>')
    main()
