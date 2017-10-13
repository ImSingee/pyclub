
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

    ADMIN_KEY = "5201314666"

    ADMIN_PASSWORD = "5201314666"

    TEST_BUILDER_KEY = "5201314666"

    DEFAULT_KEY = "5201314666"
    
    SHARING_TOKEN = "5201314666"

    # RECAPTCHA_PUBLIC_KEY = "6LdKkQQTAAAAAEH0GFj7NLg5tGicaoOus7G9Q5Uw"
    # RECAPTCHA_PRIVATE_KEY = '6LdKkQQTAAAAAMYroksPTJ7pWhobYb88fTAcxcYn'
    

