
# #coding=utf-8
# from flask import Blueprint, render_template, redirect, url_for

# #========================================================
# #main蓝图


# main_blueprint=Blueprint(
#     'main',
#     __name__,
#     template_folder='../templates/main'
#     )

# @main_blueprint.route('/')
# def index():
#     return redirect(url_for('Tiezi.home'))

# from webapp.forms import LoginForm, RegisterForm

# @main_blueprint.route('/login', method=['GET','POST'])
# def login():
#     form = LoginForm()

#     if form.validate_on_submit():
#         flash("You have been logged in.", category="success")
#         return redirect(url_for(Tiezi.home))
#     return render_template('login.html', form=form)

# @main_blueprint.route('/logout', methods=['GET','POST'])
# def logout():
#     flash("you have been logged out.", category="success")
#     return redirect(url_for('.home'))

# @main_blueprint.route('register', methods=['GET', 'Post'])
# def register():
#     form = RegisterForm()
#     if form.validate_on_submit():
#         new_user = User()
#         new_user.username = form.username.data
#         new_user.set_password(form.password.data)

#         db.session.add(new_user)
#         db.sessiom.commit()

#         flash("Your user has been careted please login", category="success")
#         return redirect(url_for('.login'))

#     return render_template('register.html', form=form)
# #=======================================================================