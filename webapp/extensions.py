


#==========================
from flask_bcrypt import Bcrypt
from flask.ext.admin import Admin
admin = Admin()
bcrypt = Bcrypt()
#========================================
from flask_login import LoginManager


login_manager = LoginManager()

login_manager.login_view = "main.login"#定义登录页视图

login_manager.session_protection = "strong"

login_manager.login_manager = "Please login to access this page"

login_manager.login_message_category = "info"

@login_manager.user_loader
def load_user(userid):
    from webapp.models import User
    return User.query.get(userid)
#user对象需要添加一些方法从而满足flask-login的需求

#=========================
from flask_principal import Principal, Permission, RoleNeed
principals = Principal()
admin_permission = Permission(RoleNeed('admin'))
poster_permission = Permission(RoleNeed('poster'))
default_permission = Permission(RoleNeed('default'))
test_builder_permission = Permission(RoleNeed('test_builder'))
