#coding=utf-8

import datetime
from os import path
from sqlalchemy import func
from flask import render_template, Blueprint
from webapp.models import db, Post, Tag, Comment, User, tags, RelatedPost, Note
from webapp.forms import CommentForm, PostForm, UserForm
from flask import redirect, url_for
from flask import g, session, abort, flash
from flask_login import login_required, current_user
from webapp.extensions import poster_permission, admin_permission
from flask_principal import Permission, UserNeed




#==================================================


def get_not_viewed_inform_num():
    try:
        if current_user.username:
            not_viewed_posts = RelatedPost.query.filter_by(is_viewed=False,
                                                         user_id=current_user.id).all()
            return len(not_viewed_posts)
        else:
            return None
    except:
        return None


def sidebar_data():

    recent = Post.query.order_by(Post.publish_date.desc()).limit(5).all()
    top_tags = db.session.query(Tag, func.count(tags.c.post_id).label('total')
                                ).join(tags).group_by(Tag).order_by(
                                'total DESC').limit(5).all()
    return recent, top_tags


def get_note():
    try:
        note = Note.query.order_by(Note.publish_date.desc()).limit(1).one()
        return note
    except:
        note = Note()
        note.text = "no message"
        note.publish_date = datetime.datetime.now()
        db.session.add(note)
        db.session.commit()
        get_note()
#==============================================================
#2博客 蓝图实例
tiezi_blueprint = Blueprint(
    'tiezi',
    __name__,
    template_folder=path.join(path.pardir, 'templates', 'tiezi'),
    static_folder=path.join(path.pardir, 'static'),
    url_prefix='/tiezi'
    )
#=======================================================
#开始每个响应之前检查会话对象看看是否存在username如果存在则添加到g对象
@tiezi_blueprint.before_request
def check_user():
    if 'username' in session:
        g.current_user = User.query.filter_by(
            username=session['username']
            ).one()
    else:
        g.current_user = None
        
#=====================================================
#4
# @tiezi_blueprint.route('/')
# def home(page=1):
#     posts = Post.query.order_by(
#         Post.publish_date.desc()
#         ).paginate(page, 10)
#     #获取侧边栏
#     recent, top_tags = sidebar_data()
    
#     #返回页面
#     pagination = Post.query.order_by(Post.publish_date.desc()).paginate(
#         page=page,
#         per_page=10
#         ) #返回该页面对象

#     endpoint_func = lambda x: url_for('tiezi.home', page=x)
#     return render_template(
#             'home.html',
#             posts=posts,
#             recent=recent,
#             top_tags=top_tags,
#             endpoint_func = endpoint_func,
#             pagination=pagination,)




@tiezi_blueprint.route('/')
@tiezi_blueprint.route("/<int:page>")
def home(page=1):


    #posts = Post.query.order_by(Post.publish_date.desc()).paginate(page, 10)
    #更据文章或者评论的动态更新，类似学校论坛
    tops = Post.query.filter_by(is_top=True, is_published=True).order_by(Post.dynamic_date.desc()).paginate(1,2)
    posts = Post.query.filter_by(is_top=False, is_published=True).order_by(Post.dynamic_date.desc()).paginate(page, 10)
    recent, top_tags = sidebar_data()
    not_viewed_inform_num = get_not_viewed_inform_num()
    note = get_note()
    return render_template(
        'home.html',
        tops=tops,
        posts=posts,
        recent=recent,
        top_tags=top_tags,
        Comment=Comment,
        not_viewed_inform_num=not_viewed_inform_num,
        note=note
    )

@tiezi_blueprint.route('/posts_renew')
@tiezi_blueprint.route('/posts_renew/<int:page>')
def posts_renew(page=1):
    #更据文章（问题）动态更新（新文章或新的问题），类似博客
    posts = Post.query.order_by(Post.publish_date.desc()).paginate(page, 10)
    # posts = Post.query.order_by(Post.dynamic_date.desc()).paginate(page, 10)
    recent, top_tags = sidebar_data()
    not_viewed_inform_num = get_not_viewed_inform_num()
    note = get_note()

    return render_template(
        'latest.html',
        posts=posts,
        recent=recent,
        top_tags=top_tags,
        not_viewed_inform_num=not_viewed_inform_num,
        note=note,
        Comment=Comment
    )



# @tiezi_blueprint.route('/new_tiezi', methods=['GET', 'POST'])
# @login_required
# #@poster_permission.require(http_exception=403)
# def new_tiezi():
#     form = PostForm()

#     if form.validate_on_submit():

#         new_post = Post(form.title.data)
#         new_post.text = form.text.data
#         now = datetime.datetime.now()
#         new_post.publish_date = now
#         new_post.dynamic_date = now
#         new_post.user = User.query.filter_by(
#             username=current_user.username
#         ).one()
#         new_post.is_published = True
#         db.session.add(new_post)
#         db.session.commit()

#         post = Post.query.filter_by(publish_date=now).one()
#         new_related_post = RelatedPost()
#         new_related_post.post_id = post.id
#         new_related_post.user_id = post.user_id
#         new_related_post.viewed_date = now
#         db.session.add(new_related_post)
#         db.session.commit()
        
#     not_viewed_inform_num = get_not_viewed_inform_num()
#     note = get_note()
#     return render_template('new_tiezi.html',
#                             form=form,
#                             not_viewed_inform_num=not_viewed_inform_num,
#                             note=note)


#===================================================
#5
#新文章

# @tiezi_blueprint.route('/new', methods=['GET', 'POST'])
# @login_required  # 用该装饰器将页面重定向到登录页
# def new_post():
#     #非作者不可以创建
#     # if 'username' not in session:
#     #     return redirect(url_for('main.login'))
#     #因为前面讲username绑定在g上
#     if not g.current_user:
#         return redirect(url_for('main.login'))

#     form = PostForm()
#     if form.validate_on_submit():
#         new_post = Post(form.title.data)
#         new_post.text = form.text.data
#         new_post.publish_date = datetime.datetime.now()

#         db.session.add(new_post)
#         db.session.commit()
#     return render_template('new.html', form=form)

@tiezi_blueprint.route('/new', methods=['GET', 'POST'])
@login_required
#@poster_permission.require(http_exception=403)
def new_post():
    form = PostForm()

    if form.validate_on_submit():

        new_post = Post(form.title.data)
        new_post.text = form.text.data
        now = datetime.datetime.now()
        new_post.publish_date = now
        new_post.dynamic_date = now
        new_post.user = User.query.filter_by(
            username=current_user.username
        ).one()
        new_post.is_published = True
        db.session.add(new_post)
        db.session.commit()
        
        
        post = Post.query.filter_by(publish_date=now).one()
        new_related_post = RelatedPost()
        new_related_post.post_id = post.id
        new_related_post.user_id = post.user_id
        new_related_post.viewed_date = now
        new_related_post.is_viewed = True
        new_related_post.is_commented_only = False
        db.session.add(new_related_post)
        db.session.commit()
        return redirect(url_for('tiezi.post', post_id=post.id))

            
    not_viewed_inform_num = get_not_viewed_inform_num()
    note = get_note()
    return render_template('new.html',
                            form=form,
                            not_viewed_inform_num=not_viewed_inform_num,
                            note=note)
#=======================================================
#编辑器


# @tiezi_blueprint.route('/edit/<int:id>', methods=['GET', 'POST'])
# def edit_post(id):

#     if not g.current_user:
#         return redirect(url_for('main.login'))

#     post = Post.query.get_or_404(id)
#     if g.current_user != post.user:
#         abort(403)
#     form = PostForm()

#     if form.validate_on_submit():
#         post.title = form.title.data
#         post.text = form.text.data
#         post.publish_date = datetime.datetime.now()

#         db.session.add(post)
#         db.session.commit()

#         return redirect(url_for('.post', post_id=post.id))
#     form.text.data = post.text
#     return render_template('edit.html', form=form, post=post)

#================================================================
#文章页面


@tiezi_blueprint.route('/post/<int:post_id>',methods=['GET','POST'])
@login_required
def post(post_id):
    form = CommentForm() # 实例化一个前面定义的CommentForm()对象
    if form.validate_on_submit():
        new_comment = Comment()  # 实例化一个Comment对象
        new_comment.name = current_user.username#form.name.data  # 读取表单数据，修改Comment对象属性
        new_comment.user_id = current_user.id
        new_comment.text = form.text.data  #
        now = datetime.datetime.now()
        new_comment.date = now
        new_comment.post_id = post_id
        
        Post.query.filter_by(id=post_id).update({'dynamic_date' : now})
        db.session.add(new_comment)
        db.session.commit()

        #将当前用户与该文章关联
        exit = RelatedPost.query.filter_by(post_id=post_id,
                                       user_id=current_user.id)
        if not exit.all():
            new_related_post = RelatedPost()
            new_related_post.post_id = post_id
            new_related_post.user_id = current_user.id
            new_related_post.viewed_date = now
            db.session.add(new_related_post)
            db.session.commit()
        else:
            exit.update({'is_viewed' : False})
            exit.update({'viewed_date' : now})
            db.session.add_all(exit)
            db.session.commit()



        
        #一旦新加评论，该篇文章用户都将视为未读过此帖子
        related_posts = RelatedPost.query.filter_by(post_id=post_id)
        if related_posts:
            related_posts.update({'is_viewed' : False})
            db.session.add_all(related_posts)

            #但是除了自己之外
            my_rel_post = RelatedPost.query.filter_by(post_id=post_id,user_id=current_user.id)
            my_rel_post.update({'is_viewed' : True})
            db.session.add_all(my_rel_post)

            db.session.commit()

   

    post = Post.query.get_or_404(post_id)
    #username = User.query.filter_by(id=post.user_id).one().username 
    tags = post.tags
    
    comments = post.comments.order_by(Comment.date.desc()).all()
    recent, top_tags = sidebar_data()
    not_viewed_inform_num = get_not_viewed_inform_num()
    note=get_note()
    try:
        if current_user.id:
            try:

                related_posts = RelatedPost.query.filter_by(user_id=current_user.id,
                                                           post_id=post_id)
                if related_posts:
                    related_posts.update({'viewed_date' : datetime.datetime.now()})
                    related_posts.update({'is_viewed' : True})
                    db.session.add(related_posts.one())
                    db.session.commit()
            except Exception as e:
                print(e)
    except:
        pass
    return render_template(
        'post.html',
        g=g,
        post=post,
        tags=tags,
        comments=comments,
        recent=recent,
        top_tags=top_tags,
        form=form,
        not_viewed_inform_num=not_viewed_inform_num,
        note=note
        )#传入表单对象

#=================================================
#文章标签
@tiezi_blueprint.route('/tag/<string:tag_name>')
def tag(tag_name):
    tag = Tag.query.fliter_by(title=tag_name).first_or_404()
    posts = tag.posts.order_by(Post.publish_date.desc()).all()
    recent, top_tags = sidebar_data()
   
    return render_template(
        'tag.html',
        tag=tag,
        posts=posts,
        recent=recent,
        top_tags=top_tags)
#================================================
#帖子作者
@login_required
@tiezi_blueprint.route('/user_admin/')
@tiezi_blueprint.route('/user_admin/<int:page1>/<int:page2>')
def user_admin(page1=1, page2=1):
    user = current_user
    try:
        posts = user.posts.order_by(Post.publish_date.desc()).paginate(page1, 5)
    except Exception as e:
        print(e)
        posts = None
    try:
        comment_related_posts = RelatedPost.query.filter_by(is_commented_only=True,
            user_id=current_user.id).paginate(page2, 5)



    except Exception as e:
        print(e)
        comment_related_posts = None
    # recent, top_tags = sidebar_data()
    not_viewed_inform_num = get_not_viewed_inform_num()
    return render_template(
        'user_admin.html',
        tag=tag,
        posts=posts,
        comment_related_posts=comment_related_posts,
        user=user,
        note=get_note(),
        Comment=Comment,
        not_viewed_inform_num=not_viewed_inform_num
        )

#基本信息
@tiezi_blueprint.route('/base_user_inform/<string:username>')
def base_user_inform(username):

    user = User.query.filter_by(username=username).first_or_404()
    note = get_note()
    not_viewed_inform_num = get_not_viewed_inform_num()

    # recent, top_tags = sidebar_data()
    return render_template(
        'base_user_inform.html',
        user=user,
        note=note,
        not_viewed_inform_num=not_viewed_inform_num
        )
        # recent=recent,
        # top_tags=top_tags)
@tiezi_blueprint.route('/user_info_setting/<string:username>')
def user_info_setting(username):

    user = User.query.filter_by(username=username).first_or_404()
    note = get_note()
    not_viewed_inform_num = get_not_viewed_inform_num()
    form = UserForm()

    # recent, top_tags = sidebar_data()
    return render_template(
        'user_info_setting.html',
        user=user,
        note=note,
        not_viewed_inform_num=not_viewed_inform_num,
        form=form
        )
# @tiezi_blueprint.route('/user/<string:username>')
# @login_required
# def user(username):
#     user = User.query.filter_by(username=username).first_or_404()
#     posts = user.posts.order_by(Post.publish_date.desc()).all()
#     # recent, top_tags = sidebar_data()

#     return render_template(
#         'user.html',
#         user=user,
#         posts=posts,
#     )

#============================================

#10一个只希望文章作者能够访问的页面
@tiezi_blueprint.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
#@poster_permission.require(http_exception=403)
def edit_post(id):
    post = Post.query.get_or_404(id)
    permission = Permission(UserNeed(post.user.id))

    #我们希望管理员可以修改任何文章
    if permission.can() or admin_permission.can():
        form = PostForm()

        if form.validate_on_submit():
            post.title = form.title.data
            post.text = form.text.data
            post.publish_date = datetime.datetime.now()

            db.session.add(post)
            db.session.commit()
            flash(u"修改成功", category="success")

            return redirect(url_for('.edit_post', id=post.id))
        form.text.data = post.text
        note = get_note()
        not_viewed_inform_num = get_not_viewed_inform_num()
        return render_template('edit.html',
                                form=form,
                                post=post,
                                note=note,
                                not_viewed_inform_num=not_viewed_inform_num
                                )
    abort(403)


#
@tiezi_blueprint.route('/edit_user_inform/<int:id>', methods=['GET', 'POST'])
@login_required
#@poster_permission.require(http_exception=403)
def edit_user_inform(id):
    user = User.query.get_or_404(id)
    permission = Permission(UserNeed(user.id))

    #我们希望管理员可以修改任何文章
    if permission.can() or admin_permission.can():
        form = UserForm()

    
        if form.validate_on_submit():
            user.nick_name = form.nick_name.data
            user.class_major = form.class_major.data
            user.blog_addr = form.blog_addr.data
            user.github_addr = form.github_addr.data
            user.description = form.description.data

            db.session.add(user)
            db.session.commit()
            flash(u"信息更新成功", category="success")

            return redirect(url_for('.edit_user_inform', id=user.id))
        form.description.data=user.description
        note = get_note()
        not_viewed_inform_num = get_not_viewed_inform_num()
        
        return render_template('user_info_setting.html',
                                form=form,
                                post=post,
                                note=note,
                                not_viewed_inform_num=not_viewed_inform_num,
                                user=user
                                )
    abort(403)



@tiezi_blueprint.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
#@poster_permission.require(http_exception=403)
def delete_post(id):
    post = Post.query.get_or_404(id)
    permission = Permission(UserNeed(post.user.id))

    #我们希望管理员可以修改任何文章
    if permission.can() or admin_permission.can():
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for('tiezi.home'))
    abort(403)

@tiezi_blueprint.route('/delete_post_user_admin/<int:id>', methods=['GET', 'POST'])
@login_required
#@poster_permission.require(http_exception=403)
def delete_post_in_user_admin(id):
    post = Post.query.get_or_404(id)
    permission = Permission(UserNeed(post.user.id))

    #我们希望管理员可以修改任何文章
    if permission.can() or admin_permission.can():
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for('tiezi.user_admin'))
    abort(403)
#=============================================
@tiezi_blueprint.route('/delete_comment/<int:id>', methods=['GET', 'POST'])
@login_required
#@poster_permission.require(http_exception=403)
def delete_comment(id):
    comment = Comment.query.get_or_404(id)
    post_id = comment.post_id
    permission = Permission(UserNeed(comment.user.id))

    #我们希望管理员可以修改任何文章
    if permission.can() or admin_permission.can():
        db.session.delete(comment)
        db.session.commit()
        return redirect(url_for('tiezi.post', post_id=post_id))
    abort(403)

@tiezi_blueprint.route('/delete_comment_in_user_admin/<int:id>', methods=['GET', 'POST'])
@login_required
#@poster_permission.require(http_exception=403)
def delete_comment_in_user_admin(id):
    comment = Comment.query.get_or_404(id)
    post_id = comment.post_id
    permission = Permission(UserNeed(comment.user.id))

    if permission.can() or admin_permission.can():
        post = comment.post
        db.session.delete(comment)
        db.session.commit()
        comments = Comment.query.filter_by(post_id=post_id, user_id=current_user.id).all()
        if not comments:
 
            related_posts = RelatedPost.query.filter_by(
                                                        is_commented_only=True,
                                                        user=current_user,
                                                        post_id=post_id
                                                        ).update({'is_commented_only' : False })
            #自动加入session
            db.session.commit()

        return redirect(url_for('tiezi.user_admin'))
    abort(403)




# @tiezi_blueprint.route('/<int:page>')
@tiezi_blueprint.route('/not_viewed')
@login_required
def not_viewed(page=1):
    #根据related_post 找到post对象

    not_viewed_inform_num = get_not_viewed_inform_num()
    note = get_note()
    related_posts = RelatedPost.query.filter_by(is_viewed=False,
        user_id=current_user.id).all()
    post_list = []
    for rp in related_posts:
        post_id = rp.post_id
        post = Post.query.filter_by(id=post_id).one()
        post_list.append(post)
    return render_template(
        'not_viewed.html',
        Comment=Comment,
        post_list = post_list,
       not_viewed_inform_num = not_viewed_inform_num,
       note=note
        )
