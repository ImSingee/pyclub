# coding=utf-8

<<<<<<< HEAD
import os, time, datetime
=======
#!/usr/bin/python
# -*- coding: utf-8-*-

import os, time, datetime 
>>>>>>> up/master
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand

from webapp import create_app
from webapp.config import Config
from webapp.models import db, User, Post, Tag, Comment, Role, Sharing, RelatedPost, SecretKey

from webapp.models import Practice, AnswerComment, Answer

from gevent.wsgi import WSGIServer

# =============================================


# ====================================================

# 应用工厂模式，这里默认使用dev配置进行=================
env = os.environ.get('WEBAPP_ENV', 'dev')
app = create_app('webapp.config.%sConfig' % env.capitalize())
# =================================
migrate = Migrate(app, db)
# ===========================

manager = Manager(app)
manager.add_command("server", Server())
manager.add_command("db", MigrateCommand)

# ========================================
# $ python manage.py db init 开始跟踪数据库变更
# $ python manage.py db migrate -m"initial migration"
# $ python manage.py db upgrade#把迁移记录应用到数据库上并改变表结构
# $ python manage.py db history#查看历史版本
# S python manage.py db downgrate 版本号 #返回版本
# 也可以尝试将迁移记录和git记录关联起来
# ==============================================

ADMIN_USERNAME = Config.ADMIN_USERNAME
ADMIN_PASSWORD = Config.ADMIN_PASSWORD

TEST_BUILDER_KEY = Config.TEST_BUILDER_KEY

ADMIN_KEY = Config.ADMIN_KEY
DEFAULT_KEY = Config.DEFAULT_KEY
SHARING_TOKEN = Config.SHARING_TOKEN


# =============================================

@manager.shell
def make_shell_context():
    return dict(app=app, db=db, User=User,
                Post=Post, Tag=Tag, Comment=Comment,
                Role=Role,
                Answer=Answer,
                AnswerComment=AnswerComment,
                Practice=Practice

                )


# =================================================

# 初始化数据库
# remember to delete the existed database.db first if you want to
# use the command to initiate the database

# 数据库初始化测试
@manager.command
def setup_db_test():
    try:
        os.remove('database.db')
        print("Success - delete database.db")
    except:
        print('Error - database.db has alredy been deleted')

    db.create_all()

    admin_role = Role('admin')
    admin_role.description = u"管理员"
    db.session.add(admin_role)

    default_role = Role('default')
    default_role.description = u"默认角色"
    db.session.add(default_role)

    # 出题人角色
    test_builder_role = Role('test_builder')
    test_builder_role.description = u"出题人"
    db.session.add(test_builder_role)

    # 第一位管理员
    admin = User(ADMIN_USERNAME)
    admin.set_password(ADMIN_PASSWORD)
    admin.roles.append(admin_role)
    admin.roles.append(default_role)
    admin.roles.append(test_builder_role)
    db.session.add(admin)

    # 管理员邀请码
    admin_key = SecretKey()
    admin_key.name = "admin_key"
    admin_key.key_string = "admin_key"
    db.session.add(admin_key)

    # 出题人邀请码
    test_builder_key = SecretKey()
    test_builder_key.name = "test_builder_key"
    test_builder_key.key_string = "test_builder_key"
    db.session.add(test_builder_key)

    # 默认用户邀请码
    default_key = SecretKey()
    default_key.name = "default_key"
    default_key.key_string = "default_key"
    db.session.add(default_key)

    s = "BODY TEXT"

    for i in range(100):
        new_post = Post("Post{}".format(i))
        new_post.user = admin
        new_post.text = s
        new_post.dynamic_date = datetime.datetime.now()
        new_post.published_date = datetime.datetime.now()
        db.session.add(new_post)
    # 创建几篇置顶文章
    for i in range(100, 112):
        new_post = Post("Post{}".format(i))
        new_post.user = admin
        new_post.text = s
        new_post.dynamic_date = datetime.datetime.now()
        new_post.published_date = datetime.datetime.now()
        new_post.is_top = True
        db.session.add(new_post)

    # 创建几个练习
    for i in range(100, 130):
        new_pracice = Practice("Practice{}".format(i))
        new_pracice.user = admin
        new_pracice.text = "this is practice"
        new_pracice.dynamic_date = datetime.datetime.now()
        new_pracice.published_date = datetime.datetime.now()
        db.session.add(new_pracice)

    # 创建几篇置顶练习
    for i in range(101, 115):
        new_pracice = Practice("Practice{}".format(i))
        new_pracice.user = admin
        new_pracice.text = "this is top practice"
        new_pracice.is_top = True
        new_pracice.dynamic_date = datetime.datetime.now()
        new_pracice.published_date = datetime.datetime.now()
        db.session.add(new_pracice)

    for i in range(200, 250):
        new_pracice = Practice("Practice{}".format(i))
        new_pracice.user = admin
        new_pracice.text = "this is qualified practice"
        new_pracice.is_top = False
        new_pracice.dynamic_date = datetime.datetime.now()
        new_pracice.published_date = datetime.datetime.now()
        db.session.add(new_pracice)

    # 创建几篇分享文章
    for i in range(30):
        new_sharing = Sharing("Sharing{}".format(i))
        new_sharing.text = "this is top sharing text"
        new_sharing.sharer = "小明"
        new_sharing.received_date = datetime.datetime.now()
        new_sharing.url = "http://zhuojiayuan.com"
        db.session.add(new_sharing)
    # 创建几个秘钥：
    s = SecretKey()
    s.name = "sharing_token"
    s.key_string = "5201314666"
    db.session.add(s)

    db.session.commit()
    print("database init done")


# 需要先删除现存的数据库
@manager.command
def setup_db_real():
    # 表初始化======================
    db.create_all()

    # 角色创立========================
    admin_role = Role('admin')
    admin_role.description = u"管理员"
    db.session.add(admin_role)

    default_role = Role('default')
    default_role.description = u"默认角色"
    db.session.add(default_role)

    # 出题人角色
    test_builder_role = Role('test_builder')
    test_builder_role.description = u"出题人"
    db.session.add(test_builder_role)

    # 第一位管理员======================
    admin = User("admin")
    admin.roles.append(admin_role)
    admin.roles.append(default_role)
    admin.roles.append(test_builder_role)
    admin.set_password(ADMIN_PASSWORD)
    db.session.add(admin)

    # 创建几个秘钥===========================
    s = SecretKey()
    s.name = "sharing_token"
    s.key_string = SHARING_TOKEN
    db.session.add(s)

    # 几个邀请、激活码=========================
    # 管理员邀请码
    admin_key = SecretKey()
    admin_key.name = "admin_key"
    admin_key.key_string = ADMIN_KEY
    db.session.add(admin_key)

    # 出题人邀请码
    test_builder_key = SecretKey()
    test_builder_key.name = "test_builder_key"
    test_builder_key.key_string = TEST_BUILDER_KEY
    db.session.add(test_builder_key)

    # 默认用户邀请码
    default_key = SecretKey()
    default_key.name = "default_key"
    default_key.key_string = DEFAULT_KEY
    db.session.add(default_key)

    # ======================
    # 第一篇文章
    new_post = Post(u"第一篇文章")
    new_post.user = admin
    new_post.text = "THIS IS the first text published by admin"
    new_post.dynamic_date = datetime.datetime.now()
    new_post.published_date = datetime.datetime.now()
    new_post.is_published = True
    db.session.add(new_post)

    # 第一篇置顶置顶文章
    new_post = Post(u"第一篇置顶文章")
    new_post.user = admin
    new_post.text = u"这是第一篇置顶文章"
    new_post.dynamic_date = datetime.datetime.now()
    new_post.published_date = datetime.datetime.now()
    new_post.is_top = True
    new_post.is_published = True
    db.session.add(new_post)

    # 第一篇练习
    new_pracice = Practice("Practice{}".format(1))
    new_pracice.user = admin
    new_pracice.text = "this is top practice"
    new_pracice.is_top = True
    new_pracice.is_qualified = True
    new_pracice.dynamic_date = datetime.datetime.now()
    new_pracice.published_date = datetime.datetime.now()
    db.session.add(new_pracice)

    db.session.commit()


def gserver_run(port):
    server = WSGIServer(('0.0.0.0', port), app)
    print('listening on port:', port)
    server.serve_forever()


@manager.command
def gserver(port=2333):
    gserver_run(port=port)

# @manager.command
# def robot():
#     print('running robot')
#     robot_run()


# =====================================================================
if __name__ == '__main__':
    manager.run()
