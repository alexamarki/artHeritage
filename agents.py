from PIL import Image
from data.content import Content
from data.bookmarks import Bookmarks
from data.posts import Posts
from flask import redirect


# <social> (ArtHeritage as a social network \/)
# -- <nolog> (No login required)
# ---- <users> (User-specific content) - User page loader agent [also related to <social><login><user>]
def user_page_loader(db_sess, user_p):
    posts = db_sess.query(Posts.post_date).filter(Posts.u_id == user_p.id).filter(Posts.is_public).order_by(
        Posts.post_date.desc())
    post_count = posts.count()
    post_time = posts.first()
    bookmarks = db_sess.query(Bookmarks.book_date).filter(Bookmarks.u_id == user_p.id).order_by(
        Bookmarks.book_date.desc())
    bookmark_count = bookmarks.count()
    bookmark_time = bookmarks.first()
    return post_count, post_time, bookmark_count, bookmark_time


# ---- </users>

# ---- <auth> (Logging in/registering) - Avatar cropper agents
def image_cropper(img, w, h):
    img_w, img_h = img.size
    return img.crop(((img_w - w) // 2, (img_h - h) // 2, (img_w + w) // 2, (img_h + h) // 2))


def image_square_thumbnail_maker(file, crop_size):
    img = Image.open(file)
    return image_cropper(img, min(img.size), min(img.size)).resize(crop_size, Image.LANCZOS)


# ---- </auth>
# -- </nolog>

# -- <login> (Login required)
# ----<actions> (User's actions on their own posts) - An agent for creating content items and checking their existence
# ------------------------------------------------- - Also here: an agent for removing posts and bookmarks
def check_existence(db_sess, item_id, query, item_obj, bkmrk=False):
    content_record = db_sess.query(Content).filter(Content.content_src == item_id).first()
    if content_record:
        if bkmrk and db_sess.query(Bookmarks).filter(Bookmarks.content_id == content_record.id).first():
            return redirect(f'/search/{query}')
        _content_id = content_record.id
        content_record.interactions += 1
    else:
        if "_iiif_image_base_url" in item_obj["_images"]:
            link = item_obj["_images"]["_iiif_image_base_url"] + 'full/!500,500/0/default.jpg'
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
        if item_obj["_primaryDate"]:
            _content_date = item_obj["_primaryDate"]
        else:
            _content_date = 'Unknown date'
        record = Content(
            content_src=item_id,
            content_img=link,
            content_title=_content_title,
            content_creator=_content_creator,
            content_date=_content_date,
            interactions=1
        )
        db_sess.add(record)
        db_sess.commit()
        _content_id = record.id
    return _content_id


def delete_agent(db_sess, table, submission_id):
    to_del = db_sess.query(table).filter(table.id == submission_id).first()
    if to_del:
        db_sess.delete(to_del)
        db_sess.commit()


# ----</actions>
# -- </login>
# </social>
