

import os
import re

from markdown import markdown
from flask import Flask, redirect, url_for

from webapp.models import db, User, Post, Tag, Comment, Role, Sharing, RelatedPost, Note, SecretKey

from webapp.models import Practice, AnswerComment, Answer

from webapp.controllers.tiezi import tiezi_blueprint
from webapp.controllers.main import main_blueprint
from webapp.controllers.sharing import sharing_blueprint
from webapp.controllers.practice import practice_blueprint_

from webapp.extensions import (bcrypt,admin)
from webapp.config import DevConfig

from flask_principal import identity_loaded, UserNeed, RoleNeed

from webapp.extensions import bcrypt,login_manager, principals

from flask_login import login_user, logout_user, login_required, current_user


from .models import db, Role, Post,Comment

from .controllers.admin import (
    CustomView,
    CustomModelView,
    CustomFileAdmin,
    PostView,
    SharingView
)
#=======================================================
#应用的工厂模式，在manage.py中控制配置环境
#env = os.environ.get('WEBAPP_ENV','dev')
#app = create_app('webapp.config.%sConfig' % env.capitalize())
#==========================================================
#一个app包含配置，扩展初始化，index路由处理，蓝图注册
#====================================================
#过滤器记得下方添加进去
#过滤器
def delete_html(string=None):
    
    for html_tag in ['<p>','</p>','<a>','</a>','<h1>','</h1>','<h2>','<div>','</div>']:
        if string:
            string = string.replace(html_tag,'')
    return string
#过滤器
def deal_time(deal_time=None):
    strings=str(deal_time).split(':')
    strings.pop(-1)
    string = ':'.join(strings)
    
    return string

#get text of html
def get_text(html=None):
    reg = r'>(.*?)</'
    pattern = re.compile(reg)
    result = pattern.findall(html)
    text = " ".join(result)
    try:
        text = text.replace('&nbsp','')
    except Exception as e:
        pass
    return text

def create_app(object_name):

    app = Flask(__name__)
    #配置
    app.config.from_object(object_name)
    app.config['SECRET_KEY'] = DevConfig.SECRECT_KEY

    #初始化数据库与插件
    db.init_app(app)
    bcrypt.init_app(app)


    login_manager.init_app(app)
    principals.init_app(app)

    admin.init_app(app)
    admin.add_view(CustomView(name='custom'))



    admin.add_view(
        CustomModelView(
            User, db.session, category='Models'
        )
    )
    admin.add_view(
        CustomModelView(
            Role, db.session, category='Models'
        )
    )
    admin.add_view(
        PostView(
            Post, db.session, category='Models'
        )
    )
    admin.add_view(
        CustomModelView(
            Comment, db.session, category='Models'
        )
    )
    admin.add_view(
        CustomModelView(
            Tag, db.session, category='Models'
        )
    )

    admin.add_view(
        CustomModelView(
            RelatedPost, db.session, category='Models'
        )
    )

    admin.add_view(
        CustomModelView(
            Note, db.session, category='Models'
        )
    )

    admin.add_view(
        CustomModelView(
            SecretKey, db.session, category='Models'
        )
    )

    admin.add_view(
        SharingView(
            Sharing, db.session, category='Models'
        )
    )

#防止误删 注释掉
    # admin.add_view(
    #     CustomFileAdmin(
    #         os.path.join(os.path.dirname(__file__), 'static'),
    #         '/static/',
    #         name='Static Files'
    #     )
    # )
    
    admin.add_view(
        CustomModelView(
            Practice, db.session, category='Models'
        )
    )
    admin.add_view(
        CustomModelView(
            AnswerComment, db.session, category='Models'
        )
    )
    admin.add_view(
        CustomModelView(
            Answer, db.session, category='Models'
        )
    )


    #蓝图注册
    app.register_blueprint(tiezi_blueprint)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(sharing_blueprint)
    app.register_blueprint(practice_blueprint_)
    
    @app.route('/')
    def index():
        return redirect(url_for('tiezi.home'))
    
    #Flask principle 需要添加一个函数，当身份发生改变时候，
    #这个函数会把需要添加的need添进这个身份对象中
    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        #set the identity user object
        identity.user = current_user

        #add the user need to the object
        if hasattr(current_user, 'id'):
            identity.provides.add(UserNeed(current_user.id))
        #add each role to the identity
        if hasattr(current_user, 'roles'):
            for role in current_user.roles:
                identity.provides.add(RoleNeed(role.name))
    #添加过滤器
    app.jinja_env.filters['delete_html']=delete_html
    app.jinja_env.filters['deal_time']=deal_time
    app.jinja_env.filters['get_text']=get_text
    app.jinja_env.filters['markdown']=markdown
    return app



if __name__ == '__main__':

    app.run()
