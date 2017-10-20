from os import path
import os
import tempfile


class GeneralConfig(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRECT_KEY = os.environ.get('SECRET_KEY', 'put your default key here')

    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')    # 默认管理员账号
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin')   # 默认管理员密码
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'root@localhost')  # 默认管理员邮箱

    ADMIN_KEY = 'JUSTFORTEST'

    pass


class ProductConfig(GeneralConfig):
    DEBUG = False

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + path.join(path.pardir, 'database.db')



class DevConfig(GeneralConfig):
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + path.join(path.pardir, 'database.db')

Config = eval('{}Config'.format(os.environ.get('WEBAPP_ENV', 'dev').capitalize()))
