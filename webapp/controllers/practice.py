#coding=utf-8

import datetime
from os import path
from sqlalchemy import func
from flask import render_template, Blueprint
from webapp.models import db, Post, Tag, Comment, User, tags, GLink, RelatedPost, Note
from webapp.forms import CommentForm, PostForm, UserForm
from flask import redirect, url_for
from flask import g, session, abort
from flask_login import login_required, current_user
from webapp.extensions import poster_permission, admin_permission
from flask_principal import Permission, UserNeed

#===========================================================
from webapp.models import Practice, AnswerComment, Answer

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
    return "test"
    # try:
    #     note = Note.query.order_by(Note.publish_date.desc()).limit(1).one()
    #     return note
    # except:
    #     note = Note()
    #     note.text = "no message"
    #     note.publish_date = datetime.datetime.now()
    #     db.session.add(note)
    #     db.session.commit()
    #     get_note()
#==============================================================
#2博客 蓝图实例
#由于practice与内置的某个函数名字冲突不得已都加个下划线
practice_blueprint_ = Blueprint(
    'practice_',
    __name__,
    template_folder=path.join(path.pardir, 'templates', 'practice'),
    static_folder=path.join(path.pardir, 'static'),
    url_prefix='/practice'
    )
#=======================================================
#开始每个响应之前检查会话对象看看是否存在username如果存在则添加到g对象
@practice_blueprint_.before_request
def check_user():
    if 'username' in session:
        g.current_user = User.query.filter_by(
            username=session['username']
            ).one()
    else:
        g.current_user = None
        
#=====================================================
@practice_blueprint_.route('/')
@practice_blueprint_.route("/<int:page>")
def home(page=1):
    # return "hello world %s" % page
    tops = Practice.query.filter_by(is_top=True).order_by(Practice.dynamic_date.desc()).paginate(1,2)
    practices = Practice.query.filter_by(is_top=False).order_by(Practice.dynamic_date.desc()).paginate(page, 10)
    recent, top_tags = sidebar_data()
    not_viewed_inform_num = get_not_viewed_inform_num()
    note = get_note()
    return render_template(
        'practices.html',
        tops=tops,
        practices=practices,
        recent=recent,
        top_tags=top_tags,
        AnswerComment=AnswerComment,
        Answer=Answer,
        not_viewed_inform_num=not_viewed_inform_num,
        note=note
    )
#===============================================================
# @practice_blueprint_.route('/new_practice', methods=['GET', 'POST'])
# @login_required
# #@poster_permission.require(http_exception=403)
# def new_practice():
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
#     return render_template('new_practice.html',
#                             form=form,
#                             not_viewed_inform_num=not_viewed_inform_num,
#                             note=note)


# #===================================================

# @practice_blueprint_.route('/new', methods=['GET', 'POST'])
# @login_required
# #@poster_permission.require(http_exception=403)
# def new_post():
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
#         db.session.add(new_post)
#         db.session.commit()
        
        
#         post = Post.query.filter_by(publish_date=now).one()
#         new_related_post = RelatedPost()
#         new_related_post.post_id = post.id
#         new_related_post.user_id = post.user_id
#         new_related_post.viewed_date = now
#         new_related_post.is_viewed = True
#         new_related_post.is_commented_only = False
#         db.session.add(new_related_post)
#         db.session.commit()
#         return redirect(url_for('practice.post', post_id=post.id))

            
#     not_viewed_inform_num = get_not_viewed_inform_num()
#     note = get_note()
#     return render_template('new.html',
#                             form=form,
#                             not_viewed_inform_num=not_viewed_inform_num,
#                             note=note)

# #================================================================
# #文章页面


@practice_blueprint_.route('/practice/<int:practice_id>',methods=['GET','POST'])
def practice(practice_id):
    return "practice_id %s" % practice_id
    # form = CommentForm() # 实例化一个前面定义的CommentForm()对象
    # if form.validate_on_submit():
    #     new_comment = Comment()  # 实例化一个Comment对象
    #     new_comment.name = current_user.username#form.name.data  # 读取表单数据，修改Comment对象属性
    #     new_comment.user_id = current_user.id
    #     new_comment.text = form.text.data  #
    #     now = datetime.datetime.now()
    #     new_comment.date = now
    #     new_comment.post_id = post_id
        
    #     Post.query.filter_by(id=post_id).update({'dynamic_date' : now})
    #     db.session.add(new_comment)
    #     db.session.commit()

    #     #将当前用户与该文章关联
    #     exit = RelatedPost.query.filter_by(post_id=post_id,
    #                                    user_id=current_user.id)
    #     if not exit.all():
    #         new_related_post = RelatedPost()
    #         new_related_post.post_id = post_id
    #         new_related_post.user_id = current_user.id
    #         new_related_post.viewed_date = now
    #         db.session.add(new_related_post)
    #         db.session.commit()
    #     else:
    #         exit.update({'is_viewed' : False})
    #         exit.update({'viewed_date' : now})
    #         db.session.add_all(exit)
    #         db.session.commit()



        
    #     #一旦新加评论，该篇文章用户都将视为未读过此帖子
    #     related_posts = RelatedPost.query.filter_by(post_id=post_id)
    #     if related_posts:
    #         related_posts.update({'is_viewed' : False})
    #         db.session.add_all(related_posts)

    #         #但是除了自己之外
    #         my_rel_post = RelatedPost.query.filter_by(post_id=post_id,user_id=current_user.id)
    #         my_rel_post.update({'is_viewed' : True})
    #         db.session.add_all(my_rel_post)

    #         db.session.commit()

   

    # post = Post.query.get_or_404(post_id)
    # #username = User.query.filter_by(id=post.user_id).one().username 
    # tags = post.tags
    
    # comments = post.comments.order_by(Comment.date.desc()).all()
    # recent, top_tags = sidebar_data()
    # not_viewed_inform_num = get_not_viewed_inform_num()
    # note=get_note()
    # try:
    #     if current_user.id:
    #         try:

    #             related_posts = RelatedPost.query.filter_by(user_id=current_user.id,
    #                                                        post_id=post_id)
    #             if related_posts:
    #                 related_posts.update({'viewed_date' : datetime.datetime.now()})
    #                 related_posts.update({'is_viewed' : True})
    #                 db.session.add(related_posts.one())
    #                 db.session.commit()
    #         except Exception as e:
    #             print(e)
    # except:
    #     pass
    # return render_template(
    #     'post.html',
    #     g=g,
    #     post=post,
    #     tags=tags,
    #     comments=comments,
    #     recent=recent,
    #     top_tags=top_tags,
    #     form=form,
    #     not_viewed_inform_num=not_viewed_inform_num,
    #     note=note
    #     )#传入表单对象

# #=================================================
# #文章标签
# @practice_blueprint_.route('/tag/<string:tag_name>')
# def tag(tag_name):
#     tag = Tag.query.fliter_by(title=tag_name).first_or_404()
#     posts = tag.posts.order_by(Post.publish_date.desc()).all()
#     recent, top_tags = sidebar_data()
   
#     return render_template(
#         'tag.html',
#         tag=tag,
#         posts=posts,
#         recent=recent,
#         top_tags=top_tags)
# #================================================
# #帖子作者
# @login_required
# @practice_blueprint_.route('/user_admin/')
# @practice_blueprint_.route('/user_admin/<int:page>')
# def user_admin(page=1):
#     user = current_user
#     try:
#         posts = user.posts.order_by(Post.publish_date.desc()).paginate(page, 5)
#     except Exception as e:
#         print(e)
#         posts = None
#     try:
#         comment_related_posts = RelatedPost.query.filter_by(is_commented_only=True,
#             user_id=current_user.id).paginate(page,5)



#     except Exception as e:
#         print(e)
#         comment_related_posts = None
#     # recent, top_tags = sidebar_data()
#     not_viewed_inform_num = get_not_viewed_inform_num()
#     return render_template(
#         'user_admin.html',
#         tag=tag,
#         posts=posts,
#         comment_related_posts=comment_related_posts,
#         user=user,
#         note=get_note(),
#         Comment=Comment,
#         not_viewed_inform_num=not_viewed_inform_num
#         )

# #基本信息
# @practice_blueprint_.route('/base_user_inform/<string:username>')
# def base_user_inform(username):

#     user = User.query.filter_by(username=username).first_or_404()
#     note = get_note()
#     not_viewed_inform_num = get_not_viewed_inform_num()

#     # recent, top_tags = sidebar_data()
#     return render_template(
#         'base_user_inform.html',
#         user=user,
#         note=note,
#         not_viewed_inform_num=not_viewed_inform_num
#         )
#         # recent=recent,
#         # top_tags=top_tags)
# @practice_blueprint_.route('/user_info_setting/<string:username>')
# def user_info_setting(username):

#     user = User.query.filter_by(username=username).first_or_404()
#     note = get_note()
#     not_viewed_inform_num = get_not_viewed_inform_num()
#     form = UserForm()

#     # recent, top_tags = sidebar_data()
#     return render_template(
#         'user_info_setting.html',
#         user=user,
#         note=note,
#         not_viewed_inform_num=not_viewed_inform_num,
#         form=form
#         )

# #============================================

# #10一个只希望文章作者能够访问的页面
# @practice_blueprint_.route('/edit/<int:id>', methods=['GET', 'POST'])
# @login_required
# #@poster_permission.require(http_exception=403)
# def edit_post(id):
#     post = Post.query.get_or_404(id)
#     permission = Permission(UserNeed(post.user.id))

#     #我们希望管理员可以修改任何文章
#     if permission.can() or admin_permission.can():
#         form = PostForm()

#         if form.validate_on_submit():
#             post.title = form.title.data
#             post.text = form.text.data
#             post.publish_date = datetime.datetime.now()

#             db.session.add(post)
#             db.session.commit()

#             return redirect(url_for('.edit_post', id=post.id))
#         form.text.data = post.text
#         note = get_note()
#         not_viewed_inform_num = get_not_viewed_inform_num()
#         return render_template('edit.html',
#                                 form=form,
#                                 post=post,
#                                 note=note,
#                                 not_viewed_inform_num=not_viewed_inform_num
#                                 )
#     abort(403)


# #
# @practice_blueprint_.route('/edit_user_inform/<int:id>', methods=['GET', 'POST'])
# @login_required
# #@poster_permission.require(http_exception=403)
# def edit_user_inform(id):
#     user = User.query.get_or_404(id)
#     permission = Permission(UserNeed(user.id))

#     #我们希望管理员可以修改任何文章
#     if permission.can() or admin_permission.can():
#         form = UserForm()

    
#         if form.validate_on_submit():
#             user.nick_name = form.nick_name.data
#             user.class_major = form.class_major.data
#             user.blog_addr = form.blog_addr.data
#             user.github_addr = form.github_addr.data
#             user.description = form.description.data

#             db.session.add(user)
#             db.session.commit()

#             return redirect(url_for('.edit_user_inform', id=user.id))
#         form.description.data=user.description
#         note = get_note()
#         not_viewed_inform_num = get_not_viewed_inform_num()
        
#         return render_template('user_info_setting.html',
#                                 form=form,
#                                 post=post,
#                                 note=note,
#                                 not_viewed_inform_num=not_viewed_inform_num,
#                                 user=user
#                                 )
#     abort(403)



# @practice_blueprint_.route('/delete/<int:id>', methods=['GET', 'POST'])
# @login_required
# #@poster_permission.require(http_exception=403)
# def delete_post(id):
#     post = Post.query.get_or_404(id)
#     permission = Permission(UserNeed(post.user.id))

#     #我们希望管理员可以修改任何文章
#     if permission.can() or admin_permission.can():
#         db.session.delete(post)
#         db.session.commit()
#         return redirect(url_for('practice.home'))
#     abort(403)

# @practice_blueprint_.route('/delete_post_user_admin/<int:id>', methods=['GET', 'POST'])
# @login_required
# #@poster_permission.require(http_exception=403)
# def delete_post_in_user_admin(id):
#     post = Post.query.get_or_404(id)
#     permission = Permission(UserNeed(post.user.id))

#     #我们希望管理员可以修改任何文章
#     if permission.can() or admin_permission.can():
#         db.session.delete(post)
#         db.session.commit()
#         return redirect(url_for('practice.user_admin'))
#     abort(403)
# #=============================================
# @practice_blueprint_.route('/delete_comment/<int:id>', methods=['GET', 'POST'])
# @login_required
# #@poster_permission.require(http_exception=403)
# def delete_comment(id):
#     comment = Comment.query.get_or_404(id)
#     post_id = comment.post_id
#     permission = Permission(UserNeed(comment.user.id))

#     #我们希望管理员可以修改任何文章
#     if permission.can() or admin_permission.can():
#         db.session.delete(comment)
#         db.session.commit()
#         return redirect(url_for('practice.post', post_id=post_id))
#     abort(403)

# @practice_blueprint_.route('/delete_comment_in_user_admin/<int:id>', methods=['GET', 'POST'])
# @login_required
# #@poster_permission.require(http_exception=403)
# def delete_comment_in_user_admin(id):
#     comment = Comment.query.get_or_404(id)
#     post_id = comment.post_id
#     permission = Permission(UserNeed(comment.user.id))

#     if permission.can() or admin_permission.can():
#         post = comment.post
#         db.session.delete(comment)
#         db.session.commit()
#         comments = Comment.query.filter_by(post_id=post_id, user_id=current_user.id).all()
#         if not comments:
 
#             related_posts = RelatedPost.query.filter_by(
#                                                         is_commented_only=True,
#                                                         user=current_user,
#                                                         post_id=post_id
#                                                         ).update({'is_commented_only' : False })
#             #自动加入session
#             db.session.commit()

#         return redirect(url_for('practice.user_admin'))
#     abort(403)




# # @practice_blueprint_.route('/<int:page>')
# @practice_blueprint_.route('/not_viewed')
# @login_required
# def not_viewed(page=1):
#     #根据related_post 找到post对象

#     not_viewed_inform_num = get_not_viewed_inform_num()
#     note = get_note()
#     related_posts = RelatedPost.query.filter_by(is_viewed=False,
#         user_id=current_user.id).all()
#     post_list = []
#     for rp in related_posts:
#         post_id = rp.post_id
#         post = Post.query.filter_by(id=post_id).one()
#         post_list.append(post)
#     return render_template(
#         'not_viewed.html',
#         Comment=Comment,
#         post_list = post_list,
#        not_viewed_inform_num = not_viewed_inform_num,
#        note=note
#         )
