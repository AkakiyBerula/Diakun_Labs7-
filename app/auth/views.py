from .. import db, SQLAlchemy
from .models import User
from .forms import RegistrationForm, LoginForm
from flask import render_template, redirect, url_for, flash
from flask_login import login_user, current_user, logout_user, login_required

from . import auth_blueprint


@auth_blueprint.route("/users")
def users():
    all_users = User.query.all()
    flag = True
    if len(all_users) == 0:
        flash("Користувачі відсутні у базі даних.", category= "warning")
        flag = False
    return render_template('auth/users.html', all_users = all_users, title = "Users", flag = flag)

@auth_blueprint.route("/register", methods = ['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash("Ви авторизовані на сайті", category="warning")
        return redirect(url_for('account'))
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        user = User(username = username, email = email, password = password)
        db.session.add(user)
        db.session.commit()
        flash(f'Створено аккаунт для користувача {form.username.data}!', category = 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form, title = 'Register')

@auth_blueprint.route("/login", methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash("Ви авторизовані на сайті", category="warning")
        return redirect(url_for('auth.account'))
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        dataEmail = User.query.filter_by(email = email).first()
        if dataEmail is None or dataEmail.verify_password(password) == False:
            flash('Не вдалося авторизуватись. Будь ласка, '
            'перевірте правильність написання електронної почти і паролю.', 
            category ='warning')
        else:
            login_user(dataEmail, remember=form.remember.data)
            flash("Авторизація пройшла успішно!", category = 'success')
            return redirect(url_for('auth.login'))
    return render_template('auth/login.html', form=form, title='Login')

@auth_blueprint.route("/logout")
def logout():
    logout_user()
    flash("Ви вийшли зі своєї сторінки!", category = "success")
    return redirect(url_for('auth.login'))

@auth_blueprint.route("/account")
@login_required
def account():
    return render_template("auth/account.html", title="account")