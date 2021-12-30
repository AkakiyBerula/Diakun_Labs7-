from .. import db, SQLAlchemy
from .models import User
from .forms import RegistrationForm, LoginForm, UpdateAccountForm, ResetPasswordForm
from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash
import os
import secrets
from PIL import Image
from datetime import datetime

from . import auth_blueprint


@auth_blueprint.route("/users")
def users():
    all_users = User.query.all()
    flag = True
    if len(all_users) == 0:
        flash("Користувачі відсутні у базі даних.", category= "warning")
        flag = False
    return render_template('users.html', all_users = all_users, title = "Users", flag = flag)

@auth_blueprint.route("/register", methods = ['GET', 'POST'])
def register():
    if current_user.is_authenticated:
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
    return render_template('register.html', form=form, title = 'Register')

@auth_blueprint.route("/login", methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
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
    return render_template('login.html', form=form, title='Login')

@auth_blueprint.route("/logout")
def logout():
    logout_user()
    flash("Ви вийшли зі своєї сторінки!", category = "success")
    return redirect(url_for('auth.login'))

@auth_blueprint.route("/account", methods = ['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Дані вашого профілю оновлені!', category='success')
        return redirect(url_for('auth.account'))
    form.username.data = current_user.username
    form.email.data = current_user.email
    form.about_me.data = current_user.about_me  
    image_file = url_for("static", filename = "profile_pics/" + current_user.image_file)
    return render_template("account.html", title="Account", image_file = image_file, form = form)

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
    output_size = (250, 250)

    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@auth_blueprint.route("/reset_password", methods=['GET', 'POST'])
@login_required
def reset_password():
    form = ResetPasswordForm()
    username = User.query.get_or_404(current_user.password)
    if form.validate_on_submit():
        current_user.password = generate_password_hash(form.new_password.data)
        db.session.commit()
        flash('Пароль змінено', category='success')
        return redirect(url_for('auth.account'))
    return render_template('reset_password.html', form = form)

@auth_blueprint.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_date = datetime.utcnow()
        db.session.commit()