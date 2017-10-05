
import datetime
from flask import Blueprint, render_template

from webapp.forms import LoginForm, RegisterForm, AdminRegisterForm
from webapp.models import User, db, Role, RelatedPost, Note, InviteCode

from os import path

from flask import redirect, url_for, g, session, abort, flash
from flask_login import login_user, logout_user, login_required, current_user

from flask import current_app

from flask_principal import (
    Identity,
    AnonymousIdentity,
    identity_changed
    )

#=========================================================


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
#===============================


main_blueprint = Blueprint(
    'main',
    __name__,
    template_folder=path.join(path.pardir, 'templates', 'main'),
    static_folder=path.join(path.pardir, 'static'),
    url_prefix="/main"
    )

#================================

@main_blueprint.route('/')
def index():
    return redirect(url_for('tiezi.home'))

# #=========================================


@main_blueprint.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).one()
        login_user(user, remember=form.remember.data)

        identity_changed.send(
            current_app._get_current_object(),
            identity=Identity(user.id)
            )
        #应用session将username写入cookie
        session['username'] = form.username.data
        flash("You have been logged in.", category="success")

        return redirect(url_for("tiezi.home"))
    return render_template('login.html',
                              form=form,
                              not_viewed_inform_num = get_not_viewed_inform_num(),
                              note=get_note())
#====================================================

@main_blueprint.route('/logout', methods=['GET', 'POST'])
def logout():
    #从cookies中去除username
    # session.pop('username', None)
    logout_user()
    identity_changed.send(
        current_app._get_current_object(),
        identity=AnonymousIdentity()
        )
    flash("you have been logged out.", category="success")
    return redirect(url_for('.login'))
    #或者直接logout
#============================================================


@main_blueprint.route('/register', methods=['GET', 'Post'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(form.username.data)

        new_user.set_password(form.password.data)
        new_user.blog_addr = 'http://'
        new_user.github_addr = 'https://github.com/'

        db.session.add(new_user)
        db.session.commit()

        flash("Your user has been careted please login", category="success")
        return redirect(url_for('.login'))

    return render_template('register.html',
                             form=form,
                             not_viewed_inform_num = get_not_viewed_inform_num(),
                             note=get_note())

@main_blueprint.route('/admin_register', methods=['GET', 'Post'])
def admin_register():
    form = AdminRegisterForm()
    if form.validate_on_submit():
        new_user = User(form.username.data)

        new_user.set_password(form.password.data)
        admin = Role.query.filter_by(name="admin").one()
        new_user.roles.append(admin)
        db.session.add(new_user)
        db.session.commit()

        flash("Your user has been careted as administrator please login", category="success")
        return redirect(url_for('.login'))

    return render_template('admin_register.html',
                            form=form,
                            not_viewed_inform_num = get_not_viewed_inform_num(),
                            note=get_note())