#!/usr/bin/env python
# coding=utf-8

import os

from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand

from webapp import create_app
from webapp.config import Config
from webapp.models import db, User, Post, Tag, Comment, Role, InviteKey

from webapp.models import Practice, AnswerComment, Answer

from gevent.wsgi import WSGIServer

env = os.environ.get('WEBAPP_ENV', 'dev')
app = create_app('webapp.config.%sConfig' % env.capitalize())

migrate = Migrate(app, db)

# ========================================
# $ python manage.py db init 开始跟踪数据库变更
# $ python manage.py db migrate -m"initial migration"
# $ python manage.py db upgrade#把迁移记录应用到数据库上并改变表结构
# $ python manage.py db history#查看历史版本
# S python manage.py db downgrate 版本号 #返回版本
# 也可以尝试将迁移记录和git记录关联起来
# ==============================================

manager = Manager(app)
manager.add_command("server", Server())
manager.add_command("db", MigrateCommand)

ADMIN_USERNAME = Config.ADMIN_USERNAME
ADMIN_PASSWORD = Config.ADMIN_PASSWORD
ADMIN_EMAIL = Config.ADMIN_EMAIL

ADMIN_KEY = Config.ADMIN_KEY


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


@manager.command
def setup_db():
    # 初始化时将会清空所有内容
    db.drop_all()
    db.create_all()

    # 建立权限系统
    admin_role = Role('admin')
    admin_role.description = u"管理员"
    db.session.add(admin_role)

    default_role = Role('default')
    default_role.description = u"默认角色"
    db.session.add(default_role)

    test_builder_role = Role('test_builder')
    test_builder_role.description = u"出题人"
    db.session.add(test_builder_role)

    # 初始化用户信息
    # 第一位管理员
    admin = User(ADMIN_USERNAME)
    admin.email = ADMIN_EMAIL
    admin.set_password(ADMIN_PASSWORD)
    admin.roles.append(admin_role)
    admin.roles.append(default_role)
    admin.roles.append(test_builder_role)
    db.session.add(admin)

    # 设置管理员管理员邀请码（临时） TODO: Deleted
    admin_key = InviteKey()
    admin_key.name = "admin_key"
    admin_key.key_string = "admin_key"
    db.session.add(admin_key)

    if env == 'dev':  # 开发环境
        pass
    elif env == 'product':  # 生产环境
        pass
    else:  # 其他
        pass

    db.session.commit()


def gserver_run(port):
    server = WSGIServer(('0.0.0.0', port), app)
    print('listening on port:', port)
    server.serve_forever()


@manager.command
def gserver(port=2333):
    gserver_run(port=port)


if __name__ == '__main__':
    manager.run()
