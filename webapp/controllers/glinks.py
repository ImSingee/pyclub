

import datetime
from os import path
import sqlite3, os

from flask import render_template, Blueprint
from webapp.models import db, User, GLink, RelatedPost, Note

from flask import redirect, url_for
from flask import g, session, abort
from flask_login import login_required, current_user






def get_note():
    try:
        note = Note.query.order_by(Note.publish_date.desc()).limit(1).one()
        if not note:
            note = Note()
            note.text = "no message"
            note.publish_date = datetime.datetime.now()
            db.session.add(note)
            db.session.commit()
            get_note()
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



glinks_blueprint = Blueprint(
    'glinks',
    __name__,
    template_folder=path.join(path.pardir, 'templates', 'glinks'),
    static_folder=path.join(path.pardir, 'static'),
    url_prefix="/glinks",
    )


@glinks_blueprint.before_request
def check_user():
    if 'username' in session:
        g.current_user = User.query.filter_by(
            username=session['username']
            ).one()
    else:
        g.current_user = None
        

@glinks_blueprint.route('/glinks')
@glinks_blueprint.route('/<int:page>')
def glinks(page=1):
    
    glinks = GLink.query.order_by(GLink.received_date.desc()).paginate(page, 10)

    not_viewed_inform_num = get_not_viewed_inform_num()
    note = get_note()
    return render_template(
        'glinks.html',
        glinks=glinks,
        not_viewed_inform_num=not_viewed_inform_num,
        note=note

    )
 


def query():
    path = os.path.abspath('.')
    glink_db_path = os.path.join(path, 'glinks.db')
    try:
        conn = sqlite3.connect(glink_db_path)
    except Exception as e:
        print(e)
    try:
        cursor = conn.cursor()
        cursor.execute('select * from glinks')
        values = cursor.fetchall()[-1]
        print(values)
        cursor.close()
        conn.close()
        return values
    except Exception as e:
        print(e)
        
def hander_date(date=None):
    strings=str(date).split('.')
    strings.pop(-1)
    string = ':'.join(strings)
    return string

@glinks_blueprint.route('/new', methods=['GET', 'POST'])
def new_glink():
    
    values = query()
    title = values[0]
    text = values[1]
    url = values[2]
    sharer = values[3]
    received_date = values[4]

    #将字符串转化为时间对象
    received_date = hander_date(received_date)

    received_date = datetime.datetime.strptime(received_date, '%Y-%m-%d %H:%M:%S')
    glink = GLink(title)

    glink.text = text
    glink.url = url
    glink.sharer = sharer
    glink.received_date = received_date

    db.session.add(glink)
    db.session.commit()
    return redirect(url_for('.glinks'))




