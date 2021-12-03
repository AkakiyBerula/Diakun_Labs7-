from app import *
from app import db, SQLAlchemy
from app.models import User
from app.forms import RegistrationForm, LoginForm
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/users")
def users():
    all_users = User.query.all()
    flag = True
    if len(all_users) == 0:
        flash("Користувачі відсутні у базі даних.", category= "warning")
        flag = False
    return render_template('users.html', all_users = all_users, title = "Users", flag = flag)

@app.route("/register", methods = ['GET', 'POST'])
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
        return redirect(url_for('login'))
    return render_template('register.html', form=form, title = 'Register')

@app.route("/login", methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash("Ви авторизовані на сайті", category="warning")
        return redirect(url_for('account'))
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
            return redirect(url_for('login'))
    return render_template('login.html', form=form, title='Login')

@app.route("/logout")
def logout():
    logout_user()
    flash("Ви вийшли зі своєї сторінки!", category = "success")
    return redirect(url_for('login'))

@app.route("/account")
@login_required
def account():
    return render_template("account.html", title="account")
    