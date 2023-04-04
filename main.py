# from flask import Flask, render_template
#
# app = Flask(__name__)
#
# @app.route('/')
# @app.route('/index')
# def index():
#     param = {}
#     param['username'] = "Ученик Яндекс.Лицея"
#     param['title'] = 'Домашняя страница'
#     return render_template('index.html', **param)
#
#
# if __name__ == '__main__':
#     app.run(port=8080, host='127.0.0.1')

from data.users import Users
from data import db_session
db_session.global_init("db/user_info.db")
user = Users()
user.name = "Пользователь 1"
user.about = "биография пользователя 1"
user.login = "email@email.ru"
db_sess = db_session.create_session()
db_sess.add(user)
db_sess.commit()