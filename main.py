from flask import Flask, render_template, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, PasswordField, BooleanField
from wtforms.validators import DataRequired
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from api_request import basic_request, configurated_request, info_get
import data.db_session as db_session
from data.users import Users
from data.content import Content
from data.bookmarks import Bookmarks
from forms.user import RegisterForm
from forms.login import LoginForm

# ! ! ! ! ! ! ! ! ! ! ! ! ! Comment clarification ! ! ! ! ! ! ! ! ! ! ! ! ! #
# This is ArtHeritage's main file, which includes all routes and the         #
#   majority of the logic required for our Flask web app.                    #
# This file in particular is commented in the following manner:              #
# --Use case 1--                                                             #
# | [code] # comment - a comment regarding a particular portion of the code, #
#                          when it's written on the same line as the code.   #
# | # > comment - the aforementioned use case, when written on a blank line. #
# --Use case 2--                                                             #
# | # '--' * n <tag> comment                                                 #
# In use case #2, <tag> is either an opening or a closing tag.               #
#   These tags are always used in pairs (<tag>code</tag>).                   #
# * Tags in our comments surround code related to a particular portion of    #
#       the app, and are supposed to improve code readability, as well as    #
#       ease troubleshooting.                                                #
# * Next to the opening tag is a comment, explaining the purpose of the code #
#       it envelops.                                                         #
# * '--' may also be used n times (n >= 0) in the beginning of a comment to  #
#       clarify the level of indentation.                                    #
# As such, the following pseudocode...                                       #
# 01| # <tag1> Tag 1 explanation                                             # 
# 02| # -- <tag1-1> Tag 1.1 explanation                                      # 
# 03| def foo():                                                             # 
# 04|   pass                                                                 # 
# 05| # -- </tag1-1>                                                         # 
# 06| # -- <tag1-2> Tag 1.2 explanation                                      # 
# 07| def bar():                                                             # 
# 08|   pass                                                                 # 
# 09| # -- </tag1-2>                                                         # 
# 10| # </tag1>                                                              # 
# 11| # <tag2> Tag 2 explanation                                             # 
# 12| def baz():                                                             # 
# 13|   pass                                                                 # 
# 14| # </tag2>                                                              # 
# ...would tell us that foo() holds the properties of tags 1 and 1.1,        #
#   bar() holds the properties of tags 1 and 1.2,                            #
#   and baz() holds the property of tag 2                                    # 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

##### note to self - should probably add a thing that saves the last searched item
##### when one navigates back to search using built-in browser nav (arrows/swipes)

#####save a login using youtube-esque session ids
############### ADD PROTECTION AGAINST SQL INJECTIONS PLSSSSSSSS

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db_session.global_init("db/user_info.db")

# <handler> Login, error handling via Flask
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(Users).get(user_id)


# </handler>

# <SE> ArtHeritage as a search engine + base website things
# -- <main>
class SearchForm(FlaskForm):
    plain_query = StringField('text', validators=[DataRequired()])
    search_btn = SubmitField('Search')


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    se_form = SearchForm()
    if se_form.plain_query.data:
        return redirect(f'/search/{se_form.plain_query.data}')
    # add check for auth to fetch name + avatar
    # return template with vars (type, name, avatar)
    return render_template('main.html', form=se_form)


@app.route('/info')
def info():
    pass
    # add check for auth to fetch name + avatar
    # return the template with info + vars


@app.route('/options')
def options():
    pass
    # add form
    # fetch cookie with configs (if none, create a blank one with the default values)
    # check for login - if logged in, use the user's personal config /only if it's differtent from others'/ instead of the browser's cached data
    # return a page with the current options selected


# -- </main>

# -- <search>
#                   from flask import request
#       http://10.1.1.1:5000/login?username=alexa&password=pw1
#                   @app.route(...)
#                   def login():
#                       username = request.args.get('username')
#                       password = request.args.get('password')    \\\\\\\//////// NEEDED FOR SEARCH PARAMETERS
@app.route('/item', methods=['GET', 'POST'])
@app.route('/search', methods=['GET', 'POST'])
@app.route('/search/<query>', methods=['GET', 'POST'])
def search(query=''):
    se_form = SearchForm()
    if se_form.plain_query.data:
        return redirect(f'/search/{se_form.plain_query.data}')
    return render_template('search.html', form=se_form, file=basic_request(query), query=query)
    # request the api to make a search
    # if no configurations are requested (base search) - use the main template, which filters out non-artworks and other junk - need to work on that later and applies a basic text search
    # if configs are provided, they are added to the search


@app.route('/item/<id>')
def item(id):
    data = info_get(id)
    dict_data = data[0]
    return render_template('item.html', file=dict_data)
    # check if provided source is a link. if not, redirect to /item or /search
    # use the source link to get data about the aforementioned item from the api
    # return the page witrh the picture, name, author, time period, current location
    # maybe a few other artworks by this person
    pass


# -- </search>
# </SE>

# <social> ArtHeritage as a social network \/
# -- <nolog> No login required
# ---- <all> Non-user specific content
@app.route('/feed/<page>')
def feed(page):
    # FETCH ALL POSTS, DESC, paged
    pass


@app.route('/top')  # top users and top (by posts + bookmarks) artworks
def top():
    # last
    pass


# ---- </all>

# ---- <users> User-specific content
@app.route('/user/<name>')
def user(name):
    db_sess = db_session.create_session()
    srchd_user = db_sess.query(Users).filter(Users.username == name).first()
    if current_user.is_authenticated and name == current_user.username:
        return redirect('/me')
    if srchd_user:
        return render_template('profile.html', my_page=False, display_id=srchd_user.id,
                               display_name=srchd_user.name,
                               username=name)
    else:
        return redirect("/")


@app.route('/user/<name>/posts/<page>')
def user_posts(name, page):
    # posts but for any user if they have profile publcity ON, with no check if a person is registered and no access to edit - can use the same template with different data
    pass


@app.route('/user/<name>/bookmarks/<page>')
def user_books(name, page):
    # bookmarks but for any user if they have profile publcity ON, with no check if a person is registered and no access to edit - can use the same template with different data
    pass


# ---- </users>

# ---- <auth> Logging in/registering
@app.route('/logreg')
def logreg():
    return render_template('logReg_prompt.html')


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    reg_form = RegisterForm()
    if reg_form.validate_on_submit():
        if reg_form.password.data != reg_form.password_repeat.data:
            return render_template('register.html', form=reg_form,
                                   message="Mismatching passwords")
        db_sess = db_session.create_session()
        if db_sess.query(Users).filter(Users.login == reg_form.login.data).first():
            return render_template('register.html', form=reg_form,
                                   message="A user with this login already exists")
        user = Users(
            name=reg_form.name.data,
            username=reg_form.username.data,
            login=reg_form.login.data,
            about=reg_form.about.data
        )
        user.set_password(reg_form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', form=reg_form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    log_form = LoginForm()
    if log_form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(Users).filter(Users.login == log_form.login.data).first()
        if user and user.check_password(log_form.password.data):
            login_user(user, remember=log_form.remember_me.data)
            return redirect("/")
        return render_template('login.html', message="Incorrect login or password",
                               form=log_form)
    return render_template('login.html', form=log_form)


# ---- </auth>
# -- </nolog>

# -- <login> Login required
# ---- <user> User's account and their own posts
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/me')
def me():
    if current_user.is_authenticated:
        return render_template('profile.html', my_page=True, display_id=current_user.id, display_name=current_user.name,
                               username=current_user.username)
    else:
        return redirect("/")


@app.route('/posts')
def my_posts():
    # check if logged in - if not, send to /register with info to redirect back to /posts after registration
    # get username of the logged in user
    # do a database search for all posts by this users, sort by date, descending -- later split into pages.
    # present posts in a scroll environment with one post taking up the whole span of the page
    # return page with posts + ability to delete posts on a post-by-post basis
    pass


@app.route('/bookmarks')
def my_books():
    # check if logged in - if not, send to /register with info to redirect back to /bookmarks after registration
    # get username of the logged in user
    # do a database search for all bookmarks by this users, sort by date, descending -- later split into pages.
    # present bookmarks in a scroll env with a few bookmark squares in each row, depending on viewbox size
    # return page with bookmarks + ability to delete any of them
    pass


@app.route('/me/options')
def profile_options():
    # check if logged in - if not, send to /register with info to redirect back to /me/options after registration
    # check the db for if there were any changes to the options template
    # if there were - fetch their config file
    # present all the options in their current state
    # return the page with a form and a var of all the options and their values in an array to be passed into the template
    pass


# ---- </user>

# ----<actions> User's actions on their own posts
@app.route('/newpost')
def create_post():
    pass  # need some way to pass artwork info to here


### not sure if the following ones should be pages, or if they can just be functions
### that restart this page. idk basically? prolly pages

# deletepost

# remove bookmark

@app.route('/add_bookmark/<item_id>', methods=['GET', 'POST'])
def add_bookmark(item_id):
    inf = info_get(item_id)
    if inf[1] == 0 or not current_user.is_authenticated:
        redirect("/")
    else:
        _content_id = ''
        db_sess = db_session.create_session()
        content_record = db_sess.query(Content).filter(Content.content_src == item_id).first()
        if content_record:
            _content_id = content_record.id
            content_record.latest_interaction += 1
        else:
            if "_iiif_image_base_url" in inf[0]["_images"]:
                link = inf[0]["_images"]["_iiif_image_base_url"] + 'full/full/0/default.jpg'
            else:
                link = '/static/img/missing.png'
            record = Content(
                content_src=item_id,
                content_img=link,
                content_title=inf[0]["_primaryTitle"],
                content_creator=inf[0]["_primaryMaker"],
                content_date=inf[0]["_primaryDate"],
                interactions=1
            )
            db_sess.add(record)
            db_sess.commit()
            _content_id = record.id
        bookmark = Bookmarks(
            content_id=_content_id,
            u_id=current_user.id,
        )
        db_sess.add(bookmark)
        db_sess.commit()


# ----</actions>

# ---- <sub> User's subscriptions / friends (aka mutuals) and their posts
@app.route('/subscriptions')
def subscriptions():
    # check if logged in - if not, send to /register with info to redirect back to this after registration
    # get username of the logged in user
    # check the list of subscriptions of this user
    pass


@app.route('/subfeed/<page>')
def myfeed_sub(page):
    # check if logged in - if not, send to /register with info to redirect back to this after registration
    # get username of the logged in user
    # check the list of subscriptions of this user
    # fetch posts by these people. sort by time (descending) + divide into pages later
    pass


@app.route('/friends')
def friends():
    # check if logged in - if not, send to /register with info to redirect back to this after registration
    # get username of the logged in user
    # check the list of subscriptions of this user, check which users have the current account in their subs too
    pass


@app.route('/friendfeed/<page>')
def myfeed_friend(page):
    # check if logged in - if not, send to /register with info to redirect back to this after registration
    # get username of the logged in user
    # check the list of subscriptions of this user, check which users have the current account in their subs too
    # fetch posts by these people. sort by time (descending) + divide into pages later
    pass


# ---- </sub>
# -- </login>
# </social>

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
