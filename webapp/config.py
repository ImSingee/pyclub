from os import path
import os
import tempfile


class GeneralConfig(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRECT_KEY = os.environ.get('SECRET_KEY', 'put your default key here')

    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')    # 默认管理员账号
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin')   # 默认管理员密码

    ADMIN_KEY = ''

    pass


class ProductConfig(GeneralConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + path.join(path.pardir, 'database.db')



class DevConfig(GeneralConfig):
    # CACHE_TYPE = 'simple'

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + path.join(path.pardir, 'database.db')



    TEST_BUILDER_KEY = "5201314666"

    DEFAULT_KEY = "5201314666"

    SHARING_TOKEN = "5201314666"

    # RECAPTCHA_PUBLIC_KEY = "6LdKkQQTAAAAAEH0GFj7NLg5tGicaoOus7G9Q5Uw"
    # RECAPTCHA_PRIVATE_KEY = '6LdKkQQTAAAAAMYroksPTJ7pWhobYb88fTAcxcYn'


Config = DevConfig
