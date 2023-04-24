import os
from PIL import Image
from flask import Flask, render_template, redirect
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from api_request import basic_request, configurated_request, info_get
import data.db_session as db_session
from data.users import Users
from data.content import Content
from data.bookmarks import Bookmarks
from data.posts import Posts
from data.subscriptions import Subscriptions
from forms.user_forms import RegisterForm, LoginForm, EditForm
from forms.post_forms import PostForm
from forms.search_forms import AdvancedForm, SearchForm
from flask import request

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

############### ADD PROTECTION AGAINST SQL INJECTIONS PLSSSSSSSS

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024
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


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    se_form = SearchForm()
    if se_form.plain_query.data:
        return redirect(f'/search?q={se_form.plain_query.data}')
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


@app.route('/search', methods=['GET', 'POST'])
def search():
    query = request.query_string.decode('UTF-8')
    se_form = SearchForm()
    ad_form = AdvancedForm()
    if se_form.plain_query.data:
        return redirect(f'/search?q={se_form.plain_query.data.strip()}')
    if ad_form.is_submitted():
        params_VnA = ['q_object_title=', 'q_object_type=', 'q_object_place', 'q_material_technique=', 'q_actor=',
                      'year_made_from=', 'year_made_to=', 'images_exist=1', 'on_display_at=', 'order_by=',
                      'order_sort=', 'page_size=']
        add = []
        row_c = 0
        for row in ad_form:
            print(row.id)
            if row.data and row.id != 'submit':
                if row.id == 'exist':
                    add.append('images_exist=1')
                else:
                    add.append(params_VnA[row_c] + row.data)
            row_c += 1
            print(row, row_c)
        if add:
            return redirect(f'/search?q={request.args.get("q")}&{"&".join(add)}')
    if len(query.split('&')) <= 1:
        return render_template('search.html', form=se_form, ad_form=ad_form, file=basic_request(query), query=query)
    else:
        return render_template('search.html', form=se_form, ad_form=ad_form, file=configurated_request(query),
                               query=query)


@app.route('/item/<id>')
def item(id):
    data = info_get(id)
    if data[1] == 0:
        return redirect('/search')
    dict_data = data[0][0]
    return render_template('item.html', file=dict_data)


# -- </search>
# </SE>

# <social> ArtHeritage as a social network \/
# -- <nolog> No login required
# ---- <all> Non-user specific content
@app.route('/feed')
@app.route('/feed/<int:page>')
def feed(page):
    db_sess = db_session.create_session()
    posts = db_sess.query(Posts).filter(Posts.is_public == True).order_by(Posts.post_date.desc()).limit(10).offset(
        (page - 1) * 10).all()
    if not posts and page != 1:
        return redirect('/feed')
    else:
        return render_template('posts.html', page_title="All posts", posts=posts, personal=False)


@app.route('/top')  # top (by posts + bookmarks) artworks
def top():
    # last
    pass


# ---- </all>

# ---- <users> User-specific content
def user_page_loader(db_sess, user_p):
    posts = db_sess.query(Posts.post_date).filter(Posts.u_id == user_p.id).filter(
        Posts.is_public == True).order_by(Posts.post_date.desc())
    post_count = posts.count()
    post_time = posts.first()
    bookmarks = db_sess.query(Bookmarks.book_date).filter(Bookmarks.u_id == user_p.id).order_by(
        Bookmarks.book_date.desc())
    bookmark_count = bookmarks.count()
    bookmark_time = bookmarks.first()
    return post_count, post_time, bookmark_count, bookmark_time


@app.route('/user/<name>')
def user(name):
    if current_user.is_authenticated and name == current_user.username:
        return redirect('/me')
    subscribed = False
    db_sess = db_session.create_session()
    srchd_user = db_sess.query(Users).filter(Users.username == name).first()
    if srchd_user:
        if current_user.is_authenticated:
            user_follow = db_sess.query(Subscriptions).filter(Subscriptions.u_follower_id == current_user.id).filter(
                Subscriptions.u_id == srchd_user.id).first()
            if user_follow:
                subscribed = True
        post_count, post_time, bookmark_count, bookmark_time = user_page_loader(db_sess, srchd_user)
        return render_template('profile.html', my_page=False, display_id=srchd_user.id,
                               display_name=srchd_user.name, about=srchd_user.about,
                               username=name, subscribed=subscribed, p_count=post_count, bm_count=bookmark_count,
                               p_time=post_time, bm_time=bookmark_time)
    else:
        return redirect("/")


@app.route('/user/<name>/posts')
@app.route('/user/<name>/posts/<int:page>')
def user_posts(name, page=1):
    if current_user.is_authenticated and name == current_user.username:
        return redirect(f'/posts/{page}')
    db_sess = db_session.create_session()
    user = db_sess.query(Users).filter(Users.username == name).first()
    if not user:
        return redirect('/feed/1')
    posts = db_sess.query(Posts).filter(Posts.u_id == user.id).filter(Posts.is_public == True).order_by(
        Posts.post_date.desc()).limit(10).offset((page - 1) * 10).all()
    if not posts and page != 1:
        return redirect(f'/user/{name}/posts')
    else:
        return render_template('posts.html', page_title=f"{name}'s posts", posts=posts, personal=False)


@app.route('/user/<name>/bookmarks')
@app.route('/user/<name>/bookmarks/<int:page>')
def user_books(name, page=1):
    if current_user.is_authenticated and name == current_user.username:
        return redirect(f'/bookmarks/{page}')
    db_sess = db_session.create_session()
    user = db_sess.query(Users).filter(Users.username == name).first()
    if not user:
        return redirect('/')
    books = db_sess.query(Bookmarks).filter(Bookmarks.u_id == user.id).order_by(
        Bookmarks.book_date.desc()).limit(20).offset((page - 1) * 20).all()
    if not books and page != 1:
        return redirect(f'/user/{name}/bookmarks')
    else:
        return render_template('bookmarks.html', page_title=f"{name}'s bookmarks", bkmrks=books, personal=False)


# ---- </users>

# ---- <auth> Logging in/registering
@app.route('/logreg')
def logreg():
    return render_template('logReg_prompt.html')


def image_cropper(img, w, h):
    img_w, img_h = img.size
    return img.crop(((img_w - w) // 2, (img_h - h) // 2, (img_w + w) // 2, (img_h + h) // 2))


def image_square_thumbnail_maker(file, crop_size):
    img = Image.open(file)
    return image_cropper(img, min(img.size), min(img.size)).resize(crop_size, Image.LANCZOS)


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
        if db_sess.query(Users).filter(Users.username == reg_form.username.data).first():
            return render_template('register.html', form=reg_form,
                                   message="A user with this username already exists")
        file = reg_form.avatar.data
        filename = 'av__blank'
        if file:
            filename = f'av_{reg_form.username.data}.png'
            pfp = image_square_thumbnail_maker(file, (500, 500))
            pfp.save(os.path.join('static/img/avatar', filename))
        user = Users(
            name=reg_form.name.data,
            username=reg_form.username.data,
            login=reg_form.login.data,
            about=reg_form.about.data,
            avatar=filename
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


@login_required
@app.route('/me')
def me():
    db_sess = db_session.create_session()
    post_count, post_time, bookmark_count, bookmark_time = user_page_loader(db_sess, current_user)
    return render_template('profile.html', my_page=True, display_id=current_user.id, display_name=current_user.name,
                           username=current_user.username, about=current_user.about, p_count=post_count,
                           bm_count=bookmark_count, p_time=post_time, bm_time=bookmark_time)


@login_required
@app.route('/posts')
@app.route('/posts/<int:page>')
def my_posts(page=1):
    db_sess = db_session.create_session()
    posts = db_sess.query(Posts).filter(Posts.u_id == current_user.id).order_by(Posts.post_date.desc()).limit(
        10).offset((page - 1) * 10).all()
    if not posts and page != 1:
        return redirect('/posts')
    else:
        return render_template('posts.html', page_title='My posts', posts=posts, personal=True)


@login_required
@app.route('/bookmarks')
@app.route('/bookmarks/<int:page>')
def my_books(page=1):
    db_sess = db_session.create_session()
    books = db_sess.query(Bookmarks).filter(Bookmarks.u_id == current_user.id).order_by(
        Bookmarks.book_date.desc()).limit(20).offset((page - 1) * 20).all()
    if not books and page != 1:
        return redirect('/bookmarks')
    else:
        return render_template('bookmarks.html', page_title="My bookmarks", bkmrks=books, personal=True)


@login_required
@app.route('/me/options', methods=['GET', 'POST'])
def profile_options():
    edit_form = EditForm(name=current_user.name, about=current_user.about)
    if edit_form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(Users).filter(Users.login == current_user.login).first()
        if not user and user.check_password(edit_form.password.data):
            return render_template('edit.html', message="Incorrect password",
                                   form=edit_form)
        file = edit_form.avatar.data
        if file:
            pfp = image_square_thumbnail_maker(file, (500, 500))
            pfp.save(os.path.join('static/img/avatar', f'av_{current_user.username}.png'))
            if user.avatar == 'av__blank':
                user.avatar = f'av_{current_user.username}'
        user.name = edit_form.name.data
        user.about = edit_form.about.data
        db_sess.commit()
        return redirect('/me')
    return render_template('edit.html', form=edit_form)


# ---- </user>

# ----<actions> User's actions on their own posts
def check_existence(db_sess, item_id, query, item_obj, bkmrk=False):
    content_record = db_sess.query(Content).filter(Content.content_src == item_id).first()
    if content_record:
        if bkmrk and db_sess.query(Bookmarks).filter(Bookmarks.content_id == content_record.id).first():
            return redirect(f'/search/{query}')
        _content_id = content_record.id
        content_record.interactions += 1
    else:
        if "_iiif_image_base_url" in item_obj["_images"]:
            link = item_obj["_images"]["_iiif_image_base_url"] + 'full/full/0/default.jpg'
        else:
            link = '/static/img/missing.png'
        if 'name' in item_obj["_primaryMaker"]:
            _content_creator = item_obj["_primaryMaker"]["name"]
        else:
            _content_creator = 'Unknown author'
        if item_obj["_primaryTitle"]:
            _content_title = item_obj["_primaryTitle"]
        else:
            _content_title = 'Unknown title'
        record = Content(
            content_src=item_id,
            content_img=link,
            content_title=_content_title,
            content_creator=_content_creator,
            content_date=item_obj["_primaryDate"],
            interactions=1
        )
        db_sess.add(record)
        db_sess.commit()
        _content_id = record.id
    return _content_id


@login_required
@app.route('/newpost', methods=['GET', 'POST'])
def create_post():
    post_form = PostForm()
    db_sess = db_session.create_session()
    item_id = request.args.get('iid')
    query = request.args.get('query').strip('"')
    if post_form.validate_on_submit():
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
            return redirect(f'/search?{query}')
        else:
            return redirect('/my_posts')
    return render_template('newpost.html', item_id=item_id, form=post_form)


@login_required
@app.route('/add_bookmark', methods=['GET', 'POST'])
def add_bookmark():
    item_id = request.args.get('iid')
    query = request.args.get('query').strip('"')
    item_obj, size = info_get(item_id)
    item_obj = item_obj[0]
    if size == 0:
        return redirect("/")
    else:
        db_sess = db_session.create_session()
        _content_id = check_existence(db_sess, item_id, query, item_obj, bkmrk=True)
        bookmark = Bookmarks(
            content_id=_content_id,
            u_id=current_user.id
        )
        db_sess.add(bookmark)
        db_sess.commit()
    return redirect(f'/search?{query}')


def delete_agent(table, id):
    db_sess = db_session.create_session()
    to_del = db_sess.query(table).filter(table.id == id).first()
    if to_del:
        db_sess.delete(to_del)
        db_sess.commit()


@login_required
@app.route('/deletepost/<int:post_id>', methods=['GET', 'POST'])
def delete_post(post_id):
    delete_agent(Posts, post_id)
    return redirect('/posts')


@login_required
@app.route('/remove_bookmark/<int:book_id>', methods=['GET', 'POST'])
def remove_book(book_id):
    delete_agent(Bookmarks, book_id)
    return redirect('/bookmarks')


# ----</actions>

# ---- <sub> User's subscriptions / friends (aka mutuals) and their posts
@login_required
@app.route('/subscribe/<user>')
def subscribe(user):
    if user == current_user.username:
        return redirect('/')
    db_sess = db_session.create_session()
    subscribe_to_id = db_sess.query(Users).filter(Users.username == user).first().id
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
    return redirect(f'/user/{user}')


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
        for user in user_follow:
            more_info = db_sess.query(Users).filter(Users.id == user.u_follower_id).first()
            subs.append((more_info.username, more_info.name, more_info.avatar))
    return render_template('userlist.html', nosubs=nosubs, users_l=subs)


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
        for user in user_follow:
            subs.append((user.users.username, user.users.name))
    return render_template('userlist.html', nosubs=nosubs, users_l=subs)


@login_required
@app.route('/subfeed')
@app.route('/subfeed/<int:page>')
def myfeed_sub(page=1):
    db_sess = db_session.create_session()
    user_follow = db_sess.query(Subscriptions).filter(Subscriptions.u_follower_id == current_user.id).all()
    if not user_follow:
        redirect('/feed')
    uids = [user.u_id for user in user_follow]
    posts = db_sess.query(Posts).filter(Posts.u_id.in_(uids)).order_by(Posts.post_date.desc()).limit(
        10).offset((page - 1) * 10).all()
    if not posts and page != 1:
        return redirect('/subfeed')
    else:
        return render_template('posts.html', page_title='My subscription feed', posts=posts, personal=False)


# @login_required
# @app.route('/friends')
# def friends():
#     pass
#
#
# @login_required
# @app.route('/friendfeed/<page>')
# def myfeed_friend(page):
#     pass


# ---- </sub>
# -- </login>
# </social>

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
