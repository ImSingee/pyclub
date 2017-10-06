
#定义输入域
#====================================
try:
    import FlaskForm
except:
    from flask_wtf import Form

from webapp.models import User, db,InviteCode
#=========================

#=============================================
from wtforms.validators import DataRequired, Length, EqualTo, URL
#========================================
from flask_wtf import Form, RecaptchaField
from wtforms import (
    widgets,
    StringField,
    TextAreaField,
    PasswordField,
    BooleanField
)
from wtforms.validators import DataRequired, Length, EqualTo, URL




class CKTextAreaWidget(widgets.TextArea):
    def __call__(self, field, **kwargs):
        kwargs.setdefault('class_', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)


class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()
#继承自Form
#定义两个输入域，用于读取数据，未来传递给Comment对象
#每个输入域由输入域名称和检验器构成
#将输入内容强制转化为字符串
#数据保存于name对象，可以通过name.data读取出来
#数据保存于text对象，可以通过text.data读取出来
#=========================================
#输入域名称可以在HTML显示出来
#DataRequired要求填写数据
#
#==================================
class UserForm(Form):

    description =TextAreaField(u'description',[Length(max=500)])

    nick_name = StringField(u'昵称', [Length(max=255)])
    class_major = StringField(u'专业&学历&入学年份',[Length(max=255)])
    
    blog_addr = StringField(u'blog URL', [Length(max=500)])
    github_addr = StringField(u'github URL',[Length(max=500)],)




class CommentForm(Form): 
 
    text = TextAreaField(u'Comment', validators=[DataRequired()])



class PostForm(Form):

    title = StringField(u'标题', [DataRequired(), Length(max=255)])

    text = TextAreaField(u'文章内容', [DataRequired()])

 


class LoginForm(Form):

    username = StringField(u'用户名', [DataRequired(), Length(max=255)])
    password = PasswordField(u'密码', [DataRequired()])
    remember = BooleanField(u"remember Me")

    def validate(self):
        #检验输入是否合法
        check_validate = super(LoginForm, self).validate()

        if not check_validate:
            return False
        #检验用户是否存在
        user = User.query.filter_by(
                           username=self.username.data
                           ).first()
        
        if not user:
            self.username.errors.append(
                              "无效的账号或者密码"
                              )
            return False

        #检验密码是否匹配
        if not user.check_password(self.password.data):
            self.username.errors.append(
                "无效的账号或者密码"
                 )
            return False
        return True

class RegisterForm(Form):
    username = StringField(u'用户名',[DataRequired(),Length(max=255)])
    password = PasswordField(u'密码',[DataRequired(),Length(min=8)])
    def validate(self):
        #检验输入是否合法
        check_validate = super(RegisterForm, self).validate()

        if not check_validate:
            return False
        #检验用户是否存在
        user = User.query.filter_by(
                           username = self.username.data
                           ).first()
        
        if user:
            self.username.errors.append(
                              u'用户名已经存在'
                              )
            return False
        return True

class AdminRegisterForm(Form):
    username = StringField(u'用户名',[DataRequired(),Length(max=255)])
    password = PasswordField(u'密码',[DataRequired(),Length(min=8)])
    invite_code = StringField(u"邀请码",[DataRequired(),Length(max=12)])
    def validate(self):
        #检验输入是否合法
        check_validate = super(AdminRegisterForm, self).validate()

        if not check_validate:
            return False
        #检验用户是否存在
        user = User.query.filter_by(
                           username = self.username.data
                           ).first()
        
        if user:
            self.username.errors.append(
                              u'用户名已经存在'
                              )
            return False
        if self.invite_code.data != InviteCode.query.filter_by(id=1).one().invite_code:
            self.invite_code.errors.append(u"邀请码不正确哦亲")
            return False
        return True

#练习
class AnswerForm(Form): 
 
    text = TextAreaField(u'试一试', validators=[DataRequired()])



class PracticeForm(Form):

    title = StringField(u'练习概要', [DataRequired(), Length(max=255)])

    text = TextAreaField(u'练习内容', [DataRequired()])

class AnswerCommentForm(Form): 
 
    text = TextAreaField(u'评论', validators=[DataRequired()])