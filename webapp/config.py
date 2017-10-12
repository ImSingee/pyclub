
from os import path
import os
import tempfile

class Config(object):
    pass
    





class ProdConfig(Config):
    pass



class DevConfig(Config):
    # CACHE_TYPE = 'simple'

    SECRECT_KEY = "\xed HV\xeb\xb3_\xa2q\xc3\x0e\xb7\xc1\xaf\xeeV\x95R'\xa4\xa2e\x91X"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + path.join(path.pardir, 'database.db')
    RECAPTCHA_PUBLIC_KEY = "6LdKkQQTAAAAAEH0GFj7NLg5tGicaoOus7G9Q5Uw"
    RECAPTCHA_PRIVATE_KEY = '6LdKkQQTAAAAAMYroksPTJ7pWhobYb88fTAcxcYn'
