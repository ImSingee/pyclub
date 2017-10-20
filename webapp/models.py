
from flask_sqlalchemy import SQLAlchemy, Pagination

from flask_login import AnonymousUserMixin
db = SQLAlchemy()

from webapp.extensions import bcrypt

#  !!!!!! 在该文件中创建了数据模型后，调用db.create_all()即可将数据模型对应表创建出来


#表格
#----------------
#user_id|role_id|
#----------------
roles = db.Table("role_users",
        db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
        )

#User对象，能够与数据库中表格对应，还应该具有验证设置密码，验证密码等方法
class User(db.Model):
    '''继承于db.Model,类的名字的小写将会是数据库中表的名字
    User类<-->user表'''
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))
    nick_name = db.Column(db.String(255))
    class_major = db.Column(db.String(255))
    description = db.Column(db.Text()) 

    blog_addr = db.Column(db.String(255))
    github_addr = db.Column(db.String(255))
    ip =  db.Column(db.String(255))


    #===========================
    #一个虚拟的列，与Post对象的外键约束建立联系
    #这样就不用再设置一个column,引用外部的即可
    posts = db.relationship('Post',
                             backref='user', 
                             lazy='dynamic')

    comments = db.relationship('Comment',
                         backref='user', 
                         lazy='dynamic')


    roles = db.relationship(
        'Role',
        secondary=roles,
        backref=db.backref('users', lazy='dynamic')
        )
    related_posts = db.relationship('RelatedPost',
                             backref='user', 
                             lazy='dynamic')

    practices = db.relationship('Practice',
                             backref='user', 
                             lazy='dynamic')

    answers = db.relationship('Answer',
                             backref='user', 
                             lazy='dynamic')

    answer_comments = db.relationship('AnswerComment',
                         backref='user', 
                         lazy='dynamic')
    #===================================



    # def __init__(self, username):
    #     self.username = username

    def __repr__(self):
        return "<User '{}'>".format(self.username)
        
    def set_password(self, password):
        
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    #网站的基础对象默认继承自AnonymousUserMixin
    #如果需要为匿名用户实现一些基本功能则可以继承自该对象
    #比如：login_mananer.anonymous_user = CustomAnonymousUser

    def is_authenticated(self):
        if isinstance(self, AnonymousUserMixin):
            return False
        else: 
            return True

    def is_active(self):
        return True

    def is_anonymous(self):
        if isinstance(self, AnonymousUserMixin):
            return True
        else:
            return False

    def get_id(self):
        return self.id

    # roles = db.relationship(
    #     'Role',
    #     secondary=roles,
    #     backref=db.backref('users',lazy='dynamic')
    #     )
    def __init__(self, username):
        self.username = username
        default = Role.query.filter_by(name="default").one()
        self.roles.append(default)

#=======================================


class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(250))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Role {}>'.format(self.name)

#====================================================================
#多对多的关联方式，创建一个db.Table对象
tags = db.Table('post_tags',
                db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
                db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')))
#=========================================================================


class Post(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255))
    is_top = db.Column(db.Boolean())
    is_published = db.Column(db.Boolean()) 
    text = db.Column(db.Text())
    publish_date = db.Column(db.DateTime())

    # anonymous = db.Column(db.Boolean())
    
    dynamic_date = db.Column(db.DateTime())
    #外键约束，强制要求user_id的字段的 值 存在于user表的 id列 中
    #保证每个post对象都会有一个可以对应的user
    user_id = db.Column(db.Integer(),
                        db.ForeignKey('user.id'))

    tags = db.relationship('Tag',
                           secondary=tags,
                           backref=db.backref('posts',lazy='dynamic')
                           )

    comments = db.relationship('Comment',
                               backref='post',
                              lazy='dynamic')
    #一对多
    related_posts = db.relationship('RelatedPost',
                             backref='post', 
                             lazy='dynamic')


    def __init__(self, title):
        self.title = title
        self.is_top = False
        self.is_published = False


    def __repr__(self):
        return "<Post '{}'>".format(self.title)






class Tag(db.Model):

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255))

    def __init__(self, title):
        self.title = title
    
    def __repr__(self):
        return"<Tag'{}'>".format(self.title)


class Comment(db.Model):

    id = db.Column(db.Integer(), primary_key=True)

    name = db.Column(db.String(255))
    user_id = db.Column(db.Integer(),
                        db.ForeignKey('user.id')) 
    text = db.Column(db.Text())
    date = db.Column(db.DateTime())
    post_id = db.Column(db.Integer(),
                        db.ForeignKey('post.id'))

    def __repr____(self):
        return "<Comment'{}'>".format(self.text[:15])



        

class Sharing(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.Text()) 
    text = db.Column(db.Text())
    sharer = db.Column(db.String(250))
    received_date = db.Column(db.DateTime())
    url = db.Column(db.Text())
    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return "<Sharing '{}'>".format(self.title)


        

class RelatedPost(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    
    user_id = db.Column(db.Integer(),
                        db.ForeignKey('user.id'))

    post_id = db.Column(db.Integer(),
                        db.ForeignKey('post.id'))

    viewed_date = db.Column(db.DateTime())

    is_viewed = db.Column(db.Boolean())
    
    #仅仅因为我评论了才与我相关，帖子不是我发的
    is_commented_only = db.Column(db.Boolean())

    def __init__(self):
        self.is_commented_only = True



    def __repr__(self):
        return "<RelatedPost '{}'>".format(self.post_id)


class Note(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    text = db.Column(db.Text())
    publish_date = db.Column(db.DateTime())
    user_id = db.Column(db.Integer(),
                        db.ForeignKey('user.id'))
    def __repr__(self):
        return "<Note '{}'>".format(self.text)


class SecretKey(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255))
    key_string = db.Column(db.String(255))
    def __repr__(self):
        return "<SecretKey '{}'>".format(self.name) 



#==========================
#练习专区

class Practice(db.Model):

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255))
    is_top = db.Column(db.Boolean())
    is_qualified = db.Column(db.Boolean())
    #对于默认用户是否可见
    is_viewed_by_default_role = db.Column(db.Boolean())  
    text = db.Column(db.Text())
    publish_date = db.Column(db.DateTime())

    # anonymous = db.Column(db.Boolean())
    
    dynamic_date = db.Column(db.DateTime())
    #外键约束，强制要求user_id的字段的 值 存在于user表的 id列 中
    #保证每个post对象都会有一个可以对应的user
    user_id = db.Column(db.Integer(),
                        db.ForeignKey('user.id'))

    answers = db.relationship('Answer',
                               backref='practice',
                              lazy='dynamic')


    def __init__(self, title):
        self.title = title
        self.is_top = False
        self.is_qualified = False
        self.is_viewed_by_default_role = False


    def __repr__(self):
        return "<Practice '{}'>".format(self.title)


class Answer(db.Model):

    id = db.Column(db.Integer(), primary_key=True)
    praise_point = db.Column(db.Integer())
    name = db.Column(db.String(255))
    user_id = db.Column(db.Integer(),
                        db.ForeignKey('user.id')) 
    text = db.Column(db.Text())
    date = db.Column(db.DateTime())
    practice_id = db.Column(db.Integer(),
                        db.ForeignKey('practice.id'))

    answer_comments = db.relationship('AnswerComment',
                               backref='answer',
                              lazy='dynamic')

    def __repr____(self):
        return "<Answer'{}'>".format(self.text[:15])


class AnswerComment(db.Model):

    id = db.Column(db.Integer(), primary_key=True)

    name = db.Column(db.String(255))
    user_id = db.Column(db.Integer(),
                        db.ForeignKey('user.id')) 
    text = db.Column(db.Text())
    date = db.Column(db.DateTime())
    answer_id = db.Column(db.Integer(),
                        db.ForeignKey('answer.id'))
    def __repr____(self):
        return "<AnswerComment'{}'>".format(self.text[:15])



      
if __name__ == '__main__':
    db.create_all()
            
#=================================================
#调用db.create_all()即可将数据模型对应表创建出来
#======================================
#user = User（username = 'fake_name'
#db.session.add(user)
#db.session.commit()
#
#===========================================
#user = User.query.first()
#user = User.query.get(1)#get by primary_key
#users = User.query.all()#查询返回全部
#users = User.query.limit(10).all()#限制返回个数
#users = User.query.order_by(User.username).all()#正序
#user = User.query.order_by(User.name.desc()).all()#逆序
#
#users = User.query.order_by(User.username.desc()).limit(10).first()

#Post.query.paginate(2,10)#查询返回第2页的内容,10个POst对象（11~20）
#eg：
#page = User.query.paginate(1,10)#返回数据对象
#page.iterms
#page.pages
#page.page
#page.has_prev#判断是否有
#page.has_next#判断是否有
#page.prev()#返回上一页pagination对象
#page.next()
#===========================================
#users = User.query.order_by(User.username.desc())fliter_by(username='fake_name').limit(2).all()
#fliter_by()接受具体得值
#user = User.query.fliter(id > 1).all()#fliter can accept any comparitive expression
#
#======================================================
#from sqlalchemy.sql.expression import not_, or_
#user = User.query.filter(or_(not_(User.password==None),User.id >=1)).first
#===========================================================
# 修改数据
#User.query.filter_by(username='fake_name').update({'password':'test'})
#db.sesssion.commit()
#==============================================
#删除数据
#user = User.query.filter_by(username='fake_name').first()
#db.session.delete(user)
#db.session.commit()
