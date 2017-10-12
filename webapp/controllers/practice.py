#coding=utf-8

import datetime
from os import path
from sqlalchemy import func
from flask import render_template, Blueprint, flash
from webapp.models import db, Post, Tag, Comment, User, tags, Note
from webapp.forms import AnswerForm, PracticeForm, AnswerCommentForm, PracticeAttrForm
from flask import redirect, url_for
from flask import g, session, abort
from flask_login import login_required, current_user
from webapp.extensions import poster_permission, admin_permission, test_builder_permission
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
@practice_blueprint_.route("/<int:qualified_page>/<int:unqualified_page>")
def home(qualified_page=1, unqualified_page=1):
    #合格且置顶
    try:
        top = Practice.query.filter_by(is_top=True, is_qualified=True).order_by(Practice.id).one()
    except Exception as e:
        print(e)

    #合格
    qualified_practices = Practice.query.filter_by(is_qualified=True, is_top=False).order_by(Practice.publish_date.desc()).paginate(qualified_page, 5)
    #不合格且不是置顶
    unqualified_practices = Practice.query.filter_by(is_qualified=False).order_by(Practice.publish_date.desc()).paginate(unqualified_page, 5)
    recent, top_tags = sidebar_data()
    not_viewed_inform_num = get_not_viewed_inform_num()
    note = get_note()
    form = PracticeAttrForm()

    return render_template(
        'practices.html',
        form=form,
        top=top,
        unqualified_practices=unqualified_practices,
        qualified_practices=qualified_practices,
        recent=recent,
        top_tags=top_tags,
        AnswerComment=AnswerComment,
        Answer=Answer,
        not_viewed_inform_num=not_viewed_inform_num,
        note=note
    )
#===============================================================
#练习的具体页面

@practice_blueprint_.route('/practice/<int:practice_id>/<int:page>', methods=['GET','POST'])
def practice(practice_id, page=1):

    form = AnswerForm()
    if form.validate_on_submit():
        new_answer = Answer()
        new_answer.name = current_user.username
        new_answer.user_id = current_user.id
        new_answer.text = form.text.data
        now = datetime.datetime.now()
        new_answer.date = now
        new_answer.practice_id = practice_id
        db.session.add(new_answer)
        db.session.commit()
        flash("解答已经成功提交.", category="success")

    practice = Practice.query.get_or_404(practice_id)
    # answers = practice.answers.order_by(Answer.date.desc()).all()
    answers = practice.answers.order_by(Answer.date.desc()).paginate(page, 10)

    #一些侧边栏
    not_viewed_inform_num = get_not_viewed_inform_num() 
    note = get_note()
    
    answer_comment_form = AnswerCommentForm()
    answer_comment_form.text.data = u'输入你的评论'

    return render_template(
        'practice.html',
        g=g,
        practice=practice,
        answers=answers,
        answer_comment_form=answer_comment_form,
        form=form,
        not_viewed_inform_num=not_viewed_inform_num,
        note=note
        )
#====================================================================
#给解答添加评论
@practice_blueprint_.route('/add_answer_comment/<int:answer_id>', methods=['GET','POST'])
def add_answer_comment(answer_id):
    answer_comment_form = AnswerCommentForm()
    if answer_comment_form.validate_on_submit():
        new_answer_comment = AnswerComment()
        new_answer_comment.name = current_user.username
        new_answer_comment.user_id = current_user.id
        new_answer_comment.text = answer_comment_form.text.data
        now = datetime.datetime.now()
        new_answer_comment.date = now
        new_answer_comment.answer_id = answer_id
        db.session.add(new_answer_comment)
        db.session.commit()
        flash("评论已经成功提交.", category="success")
    practice_id = Answer.query.filter_by(id=answer_id).one().practice_id
    return redirect(url_for('practice_.practice', practice_id=practice_id, page=1))

#====================================================================
#删除函数
@practice_blueprint_.route('/delete_practice/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_practice(id):
    practice = Practice.query.get_or_404(id)
    permission = Permission(UserNeed(practice.user.id))
    if permission.can() or admin_permission.can():
        db.session.delete(practice)
        db.session.commit()
        flash("练习已经删除.", category="success")
        return redirect(url_for('practice_.home'))
    abort(403)

@practice_blueprint_.route('/delete_answer/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_answer(id):
    answer = Answer.query.get_or_404(id)
    practice_id = answer.practice_id
    permission = Permission(UserNeed(answer.user.id))
    if permission.can() or admin_permission.can():
        db.session.delete(answer)
        db.session.commit()
        flash("回答已经删除.", category="success")
        return redirect(url_for('practice_.practice', practice_id=practice_id, page=1))
    abort(403)

#==============================================================
#几个编辑函数
@practice_blueprint_.route('/edit_practice/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_practice(id):
    practice = Practice.query.get_or_404(id)
    permission = Permission(UserNeed(practice.user.id))
    if permission.can() or admin_permission.can():
        form = PracticeForm()

        if form.validate_on_submit():
            practice.title = form.title.data
            practice.text = form.text.data
            practice.publish_date = datetime.datetime.now()

            db.session.add(practice)
            db.session.commit()
            flash("练习已经提交.", category="success")

            return redirect(url_for('.edit_practice', id=practice.id))
        form.text.data = practice.text
        note = get_note()
        not_viewed_inform_num = get_not_viewed_inform_num()
        return render_template('edit_practice.html',
                                form=form,
                                practice=practice,
                                note=note,
                                not_viewed_inform_num=not_viewed_inform_num
                                )
    abort(403)

@practice_blueprint_.route('/edit_answer/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_answer(id):
    answer = Answer.query.get_or_404(id)
    permission = Permission(UserNeed(answer.user.id))
    if permission.can() or admin_permission.can():
        form = AnswerForm()

        if form.validate_on_submit():
            answer.text = form.text.data
            answer.publish_date = datetime.datetime.now()
            db.session.add(answer)
            db.session.commit()

            return redirect(url_for('.edit_answer', id=answer.id))
        form.text.data = answer.text
        note = get_note()
        not_viewed_inform_num = get_not_viewed_inform_num()
        flash("回答已经成功提交", category="success")
        return render_template('edit_answer.html',
                                form=form,
                                answer=answer,
                                note=note,
                                not_viewed_inform_num=not_viewed_inform_num
                                )
    abort(403)
#================================================================================

@practice_blueprint_.route('/new_practice', methods=['GET', 'POST'])
@login_required
#@poster_permission.require(http_exception=403)
def new_practice():
    form = PracticeForm()

    if form.validate_on_submit():

        new_practice = Practice(form.title.data)
        new_practice.text = form.text.data
        now = datetime.datetime.now()
        new_practice.publish_date = now
        new_practice.dynamic_date = now
        new_practice.user = User.query.filter_by(
            username=current_user.username
        ).one()
        db.session.add(new_practice)
        db.session.commit()
        flash("练习已经成功提交.", category="success")
        
    not_viewed_inform_num = get_not_viewed_inform_num()
    note = get_note()
    return render_template('new_practice.html',
                            form=form,
                            not_viewed_inform_num=not_viewed_inform_num,
                            note=note)

#==========================
@practice_blueprint_.route('/alter_practice_attr/<int:id>', methods=['GET', 'POST'])
@login_required
@test_builder_permission.require(http_exception=403)
def alter_practice_attr(id):
    form = PracticeAttrForm()
    practice = Practice.query.get_or_404(id)
    if test_builder_permission.can() or admin_permission.can():
        if form.validate_on_submit():

            #仅仅留下一个置顶
            if form.is_top.data == True:
                tops = Practice.query.filter_by(is_top=True).all()
                for top in tops:
                    top.is_top = False
                    top.is_qualified = True
                    db.session.add(top)
                practice.is_top = form.is_top.data
                #能被置顶的都是通过审核的选项， 故 is_qualified设置为TRUE
                #因为表单有两个选项，但是模板中供显示在页面供用户选择的只有一个选项
                #如果不在这里设定为True，将以默认值提交
                practice.is_qualified = True   
                db.session.add(practice)

            if form.is_qualified.data == True:
                practice.is_qualified = form.is_qualified.data

            
            db.session.commit()
            flash(u"练习属性修改成功", category="success")
            return redirect(url_for(".home"))
            
        # not_viewed_inform_num = get_not_viewed_inform_num()
        # note = get_note()
        # return render_template('practices.html',
        #                         form=form,
        #                         not_viewed_inform_num=not_viewed_inform_num,
        #                         note=note)
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
