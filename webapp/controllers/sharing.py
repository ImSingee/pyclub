

import datetime
from os import path
# import sqlite3, os

from flask import render_template, Blueprint
from webapp.models import db, User, Sharing, RelatedPost, Note
from webapp.forms import SharingForm
from flask import redirect, url_for
from flask import g, session, abort, flash
from flask_login import login_required, current_user





def get_note():
    try:
        note = Note.query.order_by(Note.publish_date.desc()).limit(1).one()
        return note
    except:
        note = Note()
        note.text = "no message"
        note.publish_date = datetime.datetime.now()
        db.session.add(note)
        db.session.commit()
        get_note()


def get_not_viewed_inform_num():
    try:
        if current_user.username:
            not_viewed_posts = RelatedPost.query.filter_by(is_viewed=False,
                                                         user_id=current_user.id).all()
            return len(not_viewed_posts)
        else:
            return None
    except:
        return None

sharing_blueprint = Blueprint(
    'sharing_',
    __name__,
    template_folder=path.join(path.pardir, 'templates', 'sharing'),
    static_folder=path.join(path.pardir, 'static'),
    url_prefix="/sharing",
    )


@sharing_blueprint.before_request
def check_user():
    if 'username' in session:
        g.current_user = User.query.filter_by(
            username=session['username']
            ).one()
    else:
        g.current_user = None
        

@sharing_blueprint.route('/sharing', methods=['GET', 'POST'])
@sharing_blueprint.route('/<int:page>')
def sharing(page=1):
    
    sharings = Sharing.query.order_by(Sharing.received_date.desc()).paginate(page, 10)

    not_viewed_inform_num = get_not_viewed_inform_num()
    note = get_note()
    return render_template(
        'sharing.html',
        sharings=sharings,
        not_viewed_inform_num=not_viewed_inform_num,
        note=note

    )

@sharing_blueprint.route('/new', methods=['GET', 'POST'])
def new_sharing():

    form = SharingForm()
    print(form.validate_on_submit())
    if form.validate_on_submit():

        new_sharing = Sharing(form.title.data)
        new_sharing.sharer = form.sharer.data
        new_sharing.url = form.url.data
        new_sharing.text = form.text.data
        now = datetime.datetime.now()
        new_sharing.received_date = now
        db.session.add(new_sharing)
        db.session.commit()
        return redirect(url_for(".sharing"))
 
    not_viewed_inform_num = get_not_viewed_inform_num()
    note = get_note()

    return render_template('new_sharing.html',
                            form=form,
                            not_viewed_inform_num=not_viewed_inform_num,
                            note=note)



# def query():
#     path = os.path.abspath('.')
#     Sharing_db_path = os.path.join(path, 'sharing.db')
#     try:
#         conn = sqlite3.connect(Sharing_db_path)
#     except Exception as e:
#         print(e)
#     try:
#         cursor = conn.cursor()
#         cursor.execute('select * from sharing')
#         values = cursor.fetchall()[-1]
#         print(values)
#         cursor.close()
#         conn.close()
#         return values
#     except Exception as e:
#         print(e)
        
# def hander_date(date=None):
#     strings=str(date).split('.')
#     strings.pop(-1)
#     string = ':'.join(strings)
#     return string

# @sharing_blueprint.route('/new', methods=['GET', 'POST'])
# def new_Sharing():
    
#     values = query()
#     title = values[0]
#     text = values[1]
#     url = values[2]
#     sharer = values[3]
#     received_date = values[4]

#     #将字符串转化为时间对象
#     received_date = hander_date(received_date)

#     received_date = datetime.datetime.strptime(received_date, '%Y-%m-%d %H:%M:%S')
#     Sharing = Sharing(title)

#     Sharing.text = text
#     Sharing.url = url
#     Sharing.sharer = sharer
#     Sharing.received_date = received_date

#     db.session.add(Sharing)
#     db.session.commit()
#     return redirect(url_for('.sharing'))




