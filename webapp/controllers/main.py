
import datetime
from flask import Blueprint, render_template

from webapp.forms import LoginForm, RegisterForm, RoleActivateForm
from webapp.models import User, db, Role, RelatedPost, Note

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


# @main_blueprint.route('/register', methods=['GET', 'Post'])
# def register():
#     form = RegisterForm()
#     if form.validate_on_submit():
        # new_user = User(form.username.data)

        # new_user.set_password(form.password.data)
        # new_user.blog_addr = 'http://'
        # new_user.github_addr = 'https://github.com/'

        # db.session.add(new_user)
        # db.session.commit()

        # flash("Your user has been careted please login", category="success")
        # return redirect(url_for('.login'))

    # return render_template('register.html',
    #                          form=form,
    #                          not_viewed_inform_num = get_not_viewed_inform_num(),
    #                          note=get_note())
#================================================================================
from PIL import Image, ImageDraw, ImageFont, ImageFilter

import random

# 随机字母:
def rndChar():
    return chr(random.randint(65, 90))


# 随机颜色1:
def rndColor():
    return (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))

# 随机颜色2:
def rndColor2():
    return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))


def generate_verification_code():

    # 240 x 60:
    width = 60 * 4
    height = 60
    image = Image.new('RGB', (width, height), (255, 255, 255))
    # 创建Font对象:

    fpath = path.join('.', 'webapp', 'static', 'fonts', 'Arial.ttf')
    font = ImageFont.truetype(fpath, 36)
    # 创建Draw对象:
    draw = ImageDraw.Draw(image)
    # 填充每个像素:
    for x in range(width):
        for y in range(height):
            draw.point((x, y), fill=rndColor())
    # 输出文字:
    strings = ''
    for t in range(4):
        char = rndChar()
        draw.text((60 * t + 10, 10), char, font=font, fill=rndColor2())
        strings += char
    # 模糊:
    image = image.filter(ImageFilter.BLUR)
    image_path = path.join('.', 'webapp', 'static', 'image', 'code', 'code_img.jpg')
    image.save(image_path, 'jpeg')
    return image_path, strings
    

# import cStringIO
#     tmps = cStringIO.StringIO()
#     image.save(tmps, "jpeg")
#     res = Response()
#     res.headers.set("Content-Type", "image/JPEG;charset=UTF-8")
#     res.set_data(tmps.getvalue())
#     return res

#  <img id="verficode" src="./verficode">
#  <img id="verficode" src="./verficode" onclick="window.location.reload()">
#  <img id="verficode" src="./verficode" onclick="this.src='./verficode?d='+Math.random();" />

#==============================================================================================
#需要验证码的注册
# @main_blueprint.route('/register', methods=['GET', 'Post'])
# def register():
#     form = RegisterForm()
#     if form.validate_on_submit():
#         if 'code_text' in session and session['code_text'] != form.verify_code.data:
#             code_img, code_text = generate_verification_code()
#             session['code_text'] = code_text
#             return render_template('register.html',
#                                    form=form,
#                                    code_img=code_img,
#                                    not_viewed_inform_num=get_not_viewed_inform_num(),
#                                    note=get_note())
#         new_user = User(form.username.data)
#         new_user.set_password(form.password.data)
#         new_user.blog_addr = 'http://'
#         new_user.github_addr = 'https://github.com/'
#         try:
#             db.session.add(new_user)
#             db.session.commit()
#             flash(u"账号已经创立，请登录", category="success")
#             return redirect(url_for('.login'))
#         except:
#             print(traceback.print_exc())
#             db.session.rollback()
#             flash(u'注册失败')
#             code_img, code_text = generate_verification_code()
#             session['code_text'] = code_text
#             return render_template('register.html',
#                         form=form,
#                         code_img=code_img,
#                         not_viewed_inform_num = get_not_viewed_inform_num(),
#                         note=get_note())
#     code_img, code_text = generate_verification_code()
#     session['code_text'] = code_text
#     return render_template('register.html',
#                         form=form,
#                         code_img=code_img,
#                         not_viewed_inform_num = get_not_viewed_inform_num(),
#                         note=get_note())

@main_blueprint.route('/register', methods=['GET', 'Post'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(form.username.data)
        new_user.set_password(form.password.data)
        new_user.blog_addr = 'http://'
        new_user.github_addr = 'https://github.com/'
        try:
            db.session.add(new_user)
            db.session.commit()
            flash(u"账号已经创立，请登录", category="success")
            return redirect(url_for('.login'))
        except:
            print(traceback.print_exc())
            db.session.rollback()
            flash(u'注册失败')
            return render_template('register.html',
                        form=form,
                        not_viewed_inform_num = get_not_viewed_inform_num(),
                        note=get_note())
    return render_template('register.html',
                        form=form,
                        not_viewed_inform_num = get_not_viewed_inform_num(),
                        note=get_note())


@main_blueprint.route('/role_activate/<string:role_name>', methods=['GET', 'POST'])
@login_required
def role_activate(role_name):
    form = RoleActivateForm(role_name)
    if form.validate_on_submit():
        user = current_user
        role = Role.query.filter_by(name=role_name).one()
        user.roles.append(role)
        db.session.add(user)
        db.session.commit()

        flash("Congratulations!Your user has been careted as {}".format(role_name), category="success")
        return redirect(url_for('practice_.home'))

    return render_template('role_activate.html',
                            form=form,
                            role_name=role_name,
                            not_viewed_inform_num = get_not_viewed_inform_num(),
                            note=get_note())

# @main_blueprint.route('/admin_register', methods=['GET', 'Post'])
# def admin_register():
#     form = AdminRegisterForm()
#     if form.validate_on_submit():
#         new_user = User(form.username.data)

#         new_user.set_password(form.password.data)
#         admin = Role.query.filter_by(name="admin").one()
#         new_user.roles.append(admin)
#         db.session.add(new_user)
#         db.session.commit()

#         flash("Your user has been careted as administrator please login", category="success")
#         return redirect(url_for('.login'))

#     return render_template('admin_register.html',
#                             form=form,
#                             not_viewed_inform_num = get_not_viewed_inform_num(),
#                             note=get_note())