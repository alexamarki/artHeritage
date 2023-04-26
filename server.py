import os
from flask import Flask, render_template, redirect
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from api_request import basic_request, configurated_request, info_get
from flask import request
from werkzeug import exceptions
import data.db_session as db_session
from data.users import Users
from data.content import Content
from data.bookmarks import Bookmarks
from data.posts import Posts
from data.subscriptions import Subscriptions
from forms.user_forms import RegisterForm, LoginForm, EditForm
from forms.post_forms import PostForm
from forms.search_forms import AdvancedForm, SearchForm
from agents import user_page_loader, image_square_thumbnail_maker, check_existence, delete_agent

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

app = Flask(__name__)
app.config['SECRET_KEY'] = 'KJKjxkwh7w6%575&jBHJI(987'
app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024
db_session.global_init("db/user_info.db")


# <handler> Login, error handling via Flask
@app.errorhandler(exceptions.BadRequest)
def handle_401(_):
    return render_template('error.html', error=401)


@app.errorhandler(exceptions.BadRequest)
def handle_403(_):
    return render_template('error.html', error=403)


@app.errorhandler(exceptions.BadRequest)
def handle_404(_):
    return render_template('error.html', error=404)


@app.errorhandler(exceptions.BadRequest)
def handle_500(_):
    return render_template('error.html', error=500)


app.register_error_handler(401, handle_401)
app.register_error_handler(403, handle_403)
app.register_error_handler(404, handle_404)
app.register_error_handler(500, handle_500)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(Users).get(user_id)


# </handler>

# <SE> ArtHeritage as a search engine + base website things
# -- <main>
@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    se_form = SearchForm()
    if se_form.plain_query.data:
        return redirect(f'/search?q={se_form.plain_query.data}')
    return render_template('main.html', form=se_form, webview_title='Art Heritage Search')


@app.route('/info')
def info():
    return render_template('info.html', webview_title='About ArtHrtg')


@app.route('/search', methods=['GET', 'POST'])
@app.route('/search/<int:page>', methods=['GET', 'POST'])
def search(page=1):
    query = request.query_string.decode('UTF-8')
    se_form = SearchForm()
    ad_form = AdvancedForm()
    if se_form.plain_query.data:
        return redirect(f'/search?q={se_form.plain_query.data.strip()}')
    if ad_form.is_submitted():
        params_vna = ['q_object_title=', 'q_object_type=', 'q_object_place', 'q_material_technique=', 'q_actor=',
                      'year_made_from=', 'year_made_to=', 'images_exist=1', 'on_display_at=', 'order_by=',
                      'order_sort=', 'page_size=']
        add = []
        row_c = 0
        for row in ad_form:
            if row.data and row.id not in ('submit', 'csrf_token'):
                if row.id == 'exist':
                    add.append('images_exist=1')
                else:
                    add.append(params_vna[row_c] + str(row.data))
            row_c += 1
        if add:
            return redirect(f'/search?q={request.args.get("q")}&{"&".join(add)}')
    if len(query.split('&')) <= 1:
        file = basic_request(query, page)
    else:
        file = configurated_request(query, page)
    return render_template('search.html', form=se_form, ad_form=ad_form, file=file,
                           query=query, page=page, webview_title=f'Search - page {page}')


@app.route('/item/<obj_id>')
def item(obj_id=''):
    data = info_get(obj_id)
    if data[1] == 0:
        return redirect('/search')
    dict_data = data[0][0]
    return render_template('item.html', file=dict_data, webview_title=f'About item {obj_id}')


# -- </search>
# </SE>

# <social> ArtHeritage as a social network \/
# -- <nolog> No login required
# ---- <all> Non-user specific content
@app.route('/feed/<int:page>')
def feed(page):
    db_sess = db_session.create_session()
    posts = db_sess.query(Posts).filter(Posts.is_public).order_by(Posts.post_date.desc()).limit(10).offset(
        (page - 1) * 10).all()
    if not posts and page != 1:
        return redirect('/feed/1')
    else:
        return render_template('posts.html', page_title="All posts", posts=posts, personal=False, page=page,
                               webview_title=f'All posts - page {page}')


@app.route('/top')  # top (by posts + bookmarks) artworks
def top():
    db_sess = db_session.create_session()
    top5 = db_sess.query(Content).order_by(Content.interactions.desc()).limit(5).all()
    return render_template('images.html', page_title="Top-5 artworks", artworks=top5, webview_title='Top 5 artworks')


# ---- </all>

# ---- <users> User-specific content
@app.route('/user/<name>')
def user(name):
    if current_user.is_authenticated and name == current_user.username:
        return redirect('/me')
    subscribed = False
    db_sess = db_session.create_session()
    srchd_user = db_sess.query(Users).filter(Users.username == name).first()
    if not srchd_user:
        return redirect("/")
    if current_user.is_authenticated:
        user_follow = db_sess.query(Subscriptions).filter(Subscriptions.u_follower_id == current_user.id).filter(
            Subscriptions.u_id == srchd_user.id).first()
        if user_follow:
            subscribed = True
    post_count, post_time, bookmark_count, bookmark_time = user_page_loader(db_sess, srchd_user)
    return render_template('profile.html', my_page=False, display_id=srchd_user.id,
                           display_name=srchd_user.name, about=srchd_user.about,
                           username=name, subscribed=subscribed, p_count=post_count, bm_count=bookmark_count,
                           p_time=post_time, bm_time=bookmark_time, webview_title=f"{srchd_user.name}'s profile")


@app.route('/user/<name>/posts/<int:page>')
def user_posts(name, page=1):
    if current_user.is_authenticated and name == current_user.username:
        return redirect(f'/posts/{page}')
    db_sess = db_session.create_session()
    srchd_user = db_sess.query(Users).filter(Users.username == name).first()
    if not srchd_user:
        return redirect('/feed/1')
    posts = db_sess.query(Posts).filter(Posts.u_id == srchd_user.id).filter(Posts.is_public).order_by(
        Posts.post_date.desc()).limit(10).offset((page - 1) * 10).all()
    if not posts and page != 1:
        return redirect(f'/user/{name}/posts/1')
    return render_template('posts.html', page_title=f"{name}'s posts", posts=posts, personal=False, page=page,
                           webview_title=f"{srchd_user.name}'s posts")


@app.route('/user/<name>/bookmarks/<int:page>')
def user_books(name, page=1):
    if current_user.is_authenticated and name == current_user.username:
        return redirect(f'/bookmarks/{page}')
    db_sess = db_session.create_session()
    srchd_user = db_sess.query(Users).filter(Users.username == name).first()
    if not srchd_user:
        return redirect('/')
    books = db_sess.query(Bookmarks).filter(Bookmarks.u_id == srchd_user.id).order_by(
        Bookmarks.book_date.desc()).limit(20).offset((page - 1) * 20).all()
    if not books and page != 1:
        return redirect(f'/user/{name}/bookmarks/1')
    else:
        return render_template('bookmarks.html', page_title=f"{name}'s bookmarks", bkmrks=books, personal=False,
                               page=page, webview_title=f"{srchd_user.name}'s bookmarks")


# ---- </users>

# ---- <auth> Logging in/registering
@app.route('/logreg')
def logreg():
    return render_template('logReg_prompt.html', webview_title="Join ArtHrtg")


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    reg_form = RegisterForm()
    if not reg_form.validate_on_submit():
        return render_template('register.html', form=reg_form, webview_title='Registration')
    if reg_form.password.data != reg_form.password_repeat.data:
        return render_template('register.html', form=reg_form, message="Mismatching passwords",
                               webview_title='Registration - mismatching passwords')
    db_sess = db_session.create_session()
    if db_sess.query(Users).filter(Users.login == reg_form.login.data).first():
        return render_template('register.html', form=reg_form, message="A user with this login already exists",
                               webview_title='Registration - used email')
    if db_sess.query(Users).filter(Users.username == reg_form.username.data).first():
        return render_template('register.html', form=reg_form, message="A user with this username already exists",
                               webview_title='Registration - taken username')
    file = reg_form.avatar.data
    filename = 'av__blank'
    if file:
        filename = f'av_{reg_form.username.data}.png'
        pfp = image_square_thumbnail_maker(file, (500, 500))
        pfp.save(os.path.join('static/img/avatar', filename))
    registering_user = Users(
        name=reg_form.name.data,
        username=reg_form.username.data,
        login=reg_form.login.data,
        about=reg_form.about.data,
        avatar=filename
    )
    registering_user.set_password(reg_form.password.data)
    db_sess.add(registering_user)
    db_sess.commit()
    return redirect('/login', webview_title='Log in')


@app.route('/login', methods=['GET', 'POST'])
def login():
    log_form = LoginForm()
    if not log_form.validate_on_submit():
        return render_template('login.html', form=log_form, webview_title='Log in')
    db_sess = db_session.create_session()
    legging_user = db_sess.query(Users).filter(Users.login == log_form.login.data).first()
    if legging_user and legging_user.check_password(log_form.password.data):
        login_user(legging_user, remember=log_form.remember_me.data)
        return redirect("/")
    return render_template('login.html', message="Incorrect login or password",
                           form=log_form, webview_title="Log in - wrong password!")


# ---- </auth>
# -- </nolog>

# -- <login> Login required
# ---- <user> User's account and their own posts
@login_required
@app.route('/logout')
def logout():
    logout_user()
    return redirect("/")


@login_required
@app.route('/me')
def me():
    db_sess = db_session.create_session()
    post_count, post_time, bookmark_count, bookmark_time = user_page_loader(db_sess, current_user)
    return render_template('profile.html', my_page=True, display_id=current_user.id, display_name=current_user.name,
                           username=current_user.username, about=current_user.about, p_count=post_count,
                           bm_count=bookmark_count, p_time=post_time, bm_time=bookmark_time, webview_title="My page")


@login_required
@app.route('/posts/<int:page>')
def my_posts(page=1):
    db_sess = db_session.create_session()
    posts = db_sess.query(Posts).filter(Posts.u_id == current_user.id).order_by(Posts.post_date.desc()).limit(
        10).offset((page - 1) * 10).all()
    if not posts and page != 1:
        return redirect('/posts/1')
    else:
        return render_template('posts.html', page_title='My posts', posts=posts, personal=True, page=page,
                               webview_title='My posts')


@login_required
@app.route('/bookmarks/<int:page>')
def my_books(page=1):
    db_sess = db_session.create_session()
    books = db_sess.query(Bookmarks).filter(Bookmarks.u_id == current_user.id).order_by(
        Bookmarks.book_date.desc()).limit(20).offset((page - 1) * 20).all()
    if not books and page != 1:
        return redirect('/bookmarks/1')
    else:
        return render_template('bookmarks.html', page_title="My bookmarks", bkmrks=books, personal=True, page=page,
                               webview_title='My bookmarks')


@login_required
@app.route('/me/options', methods=['GET', 'POST'])
def profile_options():
    edit_form = EditForm(name=current_user.name, about=current_user.about)
    if edit_form.validate_on_submit():
        db_sess = db_session.create_session()
        srchd_user = db_sess.query(Users).filter(Users.login == current_user.login).first()
        if not srchd_user and srchd_user.check_password(edit_form.password.data):
            return render_template('edit.html', message="Incorrect password",
                                   form=edit_form)
        file = edit_form.avatar.data
        if file:
            pfp = image_square_thumbnail_maker(file, (500, 500))
            pfp.save(os.path.join('static/img/avatar', f'av_{current_user.username}.png'))
            if srchd_user.avatar == 'av__blank':
                srchd_user.avatar = f'av_{current_user.username}'
        srchd_user.name = edit_form.name.data
        srchd_user.about = edit_form.about.data
        db_sess.commit()
        return redirect('/me')
    return render_template('edit.html', form=edit_form, webview_title='Edit my profile')


# ---- </user>

# ----<actions> User's actions on their own posts
@login_required
@app.route('/newpost', methods=['GET', 'POST'])
def create_post():
    post_form = PostForm()
    db_sess = db_session.create_session()
    item_id = request.args.get('iid')
    page = ''
    query = ''
    if request.args.get('query'):
        page = request.args.get('page')
        query = request.args.get('query').strip('"')
    if not post_form.validate_on_submit():
        return render_template('newpost.html', item_id=item_id, form=post_form, webview_title='New post')
    _u_title = post_form.title.data
    _u_content = post_form.content.data
    _is_public = post_form.public.data
    if request.args.get('iid'):
        item_obj, size = info_get(item_id)
        item_obj = item_obj[0]
        if size == 0:
            return redirect("/")
        else:
            _content_id = check_existence(db_sess, item_id, query, item_obj)
            post = Posts(
                content_id=_content_id,
                u_id=current_user.id,
                u_title=_u_title,
                u_content=_u_content,
                is_public=_is_public
            )
    else:
        post = Posts(
            u_id=current_user.id,
            u_title=_u_title,
            u_content=_u_content,
            is_public=_is_public
        )
    db_sess.add(post)
    db_sess.commit()
    if query:
        return redirect(f'/search/{page}?{query}')
    else:
        return redirect('/posts/1')


@login_required
@app.route('/add_bookmark', methods=['GET', 'POST'])
def add_bookmark():
    item_id = request.args.get('iid')
    page = ''
    query = ''
    if request.args.get('query'):
        page = request.args.get('page')
        query = request.args.get('query').strip('"')
    item_obj, size = info_get(item_id)
    item_obj = item_obj[0]
    if size == 0:
        return redirect("/")
    db_sess = db_session.create_session()
    _content_id = check_existence(db_sess, item_id, query, item_obj, bkmrk=True)
    bookmark = Bookmarks(
        content_id=_content_id,
        u_id=current_user.id
    )
    db_sess.add(bookmark)
    db_sess.commit()
    if query:
        return redirect(f'/search/{page}?{query}')
    else:
        return redirect('/')


@login_required
@app.route('/deletepost/<int:post_id>', methods=['GET', 'POST'])
def delete_post(post_id):
    db_sess = db_session.create_session()
    delete_agent(db_sess, Posts, post_id)
    return redirect('/posts/1')


@login_required
@app.route('/remove_bookmark/<int:book_id>', methods=['GET', 'POST'])
def remove_book(book_id):
    db_sess = db_session.create_session()
    delete_agent(db_sess, Bookmarks, book_id)
    return redirect('/bookmarks/1')


# ----</actions>

# ---- <sub> User's subscriptions / friends (aka mutuals) and their posts
@login_required
@app.route('/subscribe/<user>')
def subscribe(user_to_sub_to):
    if user_to_sub_to == current_user.username:
        return redirect('/')
    db_sess = db_session.create_session()
    subscribe_to_id = db_sess.query(Users).filter(Users.username == user_to_sub_to).first().id
    user_follow = db_sess.query(Subscriptions).filter(Subscriptions.u_follower_id == current_user.id).filter(
        Subscriptions.u_id == subscribe_to_id).first()
    if not user_follow:
        subscription = Subscriptions(
            u_id=subscribe_to_id,
            u_follower_id=current_user.id
        )
        db_sess.add(subscription)
    else:
        db_sess.delete(user_follow)
    db_sess.commit()
    return redirect(f'/user/{user_to_sub_to}')


@login_required
@app.route('/subscribers')
def subscribers():
    nosubs = False
    subs = []
    db_sess = db_session.create_session()
    user_follow = db_sess.query(Subscriptions).filter(Subscriptions.u_id == current_user.id).all()
    if not user_follow:
        nosubs = True
    else:
        for follower in user_follow:
            more_info = db_sess.query(Users).filter(Users.id == follower.u_follower_id).first()
            subs.append((more_info.username, more_info.name, more_info.avatar))
    return render_template('userlist.html', nosubs=nosubs, users_l=subs, ppl_assoc='My subscribers',
                           webview_title='My subscribers')


@login_required
@app.route('/subscriptions')
def subscriptions():
    nosubs = False
    subs = []
    db_sess = db_session.create_session()
    user_follow = db_sess.query(Subscriptions).filter(Subscriptions.u_follower_id == current_user.id).all()
    if not user_follow:
        nosubs = True
    else:
        for following in user_follow:
            subs.append((following.users.username, following.users.name, following.users.avatar))
    return render_template('userlist.html', nosubs=nosubs, users_l=subs, ppl_assoc='My subscriptions',
                           webview_title='My subscriptions')


@login_required
@app.route('/subfeed/<int:page>')
def myfeed_sub(page=1):
    db_sess = db_session.create_session()
    user_follow = db_sess.query(Subscriptions).filter(Subscriptions.u_follower_id == current_user.id).all()
    if not user_follow:
        redirect('/feed')
    uids = [following.u_id for following in user_follow]
    posts = db_sess.query(Posts).filter(Posts.u_id.in_(uids)).order_by(Posts.post_date.desc()).limit(
        10).offset((page - 1) * 10).all()
    if not posts and page != 1:
        return redirect('/subfeed/1')
    else:
        return render_template('posts.html', page_title='My subscription feed', posts=posts, personal=False, page=page,
                               webview_title=f'My feed - page {page}')


# ---- </sub>
# -- </login>
# </social>

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
