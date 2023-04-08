from flask import Flask, render_template

# # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Comment clarification!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! # #
# This is ArtHeritage's main file, which includes all routes and the majority of the logic required                    #
#   for our Flask web app.                                                                                             #
# This file in particular is commented in the following manner:                                                        #
# --Use case 1--                                                                                                       #
# | [code] # comment - a comment regarding a particular portion of the code, if written on the same line as the code   #
# | # > comment - the aforementioned use case, when written on a blank line                                            #
# --Use case 2--                                                                                                       #
# | # '--' * n <tag> comment                                                                                           #
# In use case #2, <tag> is either an opening or a closing tag. These tags are used in pairs (<tag>code</tag>).         #
# * Tags in our comments surround code related to a particular portion of the app, and are supposed to                 #
#       improve code readability, as well as make troubleshooting easier.                                              #
# * Next to the opening tag is a comment, explaining the purpose of the code it envelops.                              #
# * '--' may also be used n times (n >= 0) in the beginning of a comment to clarify the level of indentation,          #
#       akin to python indentation rules. As such, the following pseudocode...                                         #
# 01| # <tag1> Tag 1 explanation                                                                                       #
# 02| # -- <tag1-1> Tag 1.1 explanation                                                                                #
# 03| def foo():                                                                                                       #
# 04|   pass                                                                                                           #
# 05| # -- </tag1-1>                                                                                                   #
# 06| # -- <tag1-2> Tag 1.2 explanation                                                                                #
# 07| def bar():                                                                                                       #
# 08|   pass                                                                                                           #
# 09| # -- </tag1-2>                                                                                                   #
# 10| # </tag1>                                                                                                        #
# 11| # <tag2> Tag 2 explanation                                                                                       #
# 12| def baz():                                                                                                       #
# 13|   pass                                                                                                           #
# 14| # </tag2>                                                                                                        #
# ...would tell us that foo() holds the properties of tags 1 and 1.1, bar() holds the properties of tags 1 and 1.2,    #
#   and baz() holds the property of tag 2                                                                              #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

app = Flask(__name__)


# <SE> ArtHeritage as a search engine + base website things

# -- <
@app.route('/')
@app.route('/home')
def home():
    pass


@app.route('/options')
def options():
    pass


# </SE>

# <social> ArtHeritage as a social network \/

# -- <nolog> No login required

# ---- <all> Non-user specific content
@app.route('/feed/<page>')
def feed(page):
    pass


@app.route('/top')  # top users and top (by posts + bookmarks) artworks
def top():
    pass


# ---- </all>

# ---- <users> User-specific content
@app.route('/user/<name>')
def user(name):
    pass


@app.route('/user/<name>/posts/<page>')
def user_posts(name, page):
    pass


@app.route('/user/<name>/bookmarks/<page>')
def user_posts(name, page):
    pass


# ---- </users>

# -- </nolog>

# -- <login> Login required

# ---- <user> User's account and their own posts

@app.route('/me')
def me():
    pass


@app.route('/posts')
def my_posts():
    pass


@app.route('/bookmarks')
def my_posts():
    pass


@app.route('/me/options')
def profile_options():
    pass


# ---- </user>

# ---- <sub> User's subscriptions / friends (aka mutuals) and their posts

@app.route('/subscriptions')
def subscriptions():
    pass


@app.route('/subfeed/<page>')
def myfeed_sub(page):
    pass


@app.route('/friends')
def friends():
    pass


@app.route('/friendfeed/<page>')
def myfeed_friend(page):
    pass


# ---- </sub>

# -- </login>

# </social>

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')

# from data.users import Users
# from data import db_session
# db_session.global_init("db/user_info.db")
# user = Users()
# user.name = "Пользователь 1"
# user.about = "биография пользователя 1"
# user.login = "email@email.ru"
# db_sess = db_session.create_session()
# db_sess.add(user)
# db_sess.commit()
