from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError, TextAreaField
from wtforms.validators import Length, DataRequired, Email, EqualTo, Regexp
from flask_login import current_user
from werkzeug.security import check_password_hash
import email_validator
from .models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', 
                            validators=
                            [Length(min=4, max=25, 
                            message = 'Це поле має бути довжиною між 4 та 25 символів.'), 
                            DataRequired(message ="Це поле обов'язкове."),
                            Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                            "Ім'я користувача може мати тільки Великі і малі латинські літери, цифри,"
                            "крапки і нижнє підкреслення.")])
    email = StringField('Email', validators=[
                        Email(message="Неправильно вказана електронна пошта."), 
                        DataRequired(message = "Це поле обов'язкове.")])
    password = PasswordField('Password', 
                            validators=[Length(min=6, 
                            message = 'Це поле має бути більше 6 символів.'), 
                            DataRequired(message = "Це поле обов'язкове.")])
    confirm_password = PasswordField('Confirm Password', 
                validators=[DataRequired(message = "Це поле обов'язкове."), 
                EqualTo('password')])
    submit = SubmitField('Sign up')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Електронна пошта уже зареєстрована.")

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Ім'я користувача уже використовується.")

    


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
                                DataRequired(message = "Це поле обов'язкове"), 
                                Email(message="Неправильно вказана електронна пошта")])
    password = PasswordField('Password', validators=[
                                        DataRequired(message = "Це поле обов'язкове")])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(message="Це поле обов'язкове"), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(message = "Це поле обов'язкове"),
                                            Email(message="Неправильно вказана електронна пошта."),])

    picture = FileField('Оновити аватар профілю', validators=[FileAllowed(['jpg', 'png'])])                 
    about_me = TextAreaField('Про мене', validators=[DataRequired(), Length(max=500)])
   
    submit = SubmitField('Оновити')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("Це ім'я користувача використовується. Будь ласка введіть інше.")

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(username=email.data).first()
            if user:
                raise ValidationError('Цей email використовується. Будь ласка виберіть іншу')

class ResetPasswordForm(FlaskForm):
    old_password = PasswordField('Старий пароль', validators=[DataRequired(message = "Це поле обов'язкове")])

    new_password = PasswordField('Новий пароль', 
                        validators=[DataRequired(message = "Це поле обов'язкове"),
                            Length(min=6, message='Пароль мусить мати не менше 6 символів')])

    repeat_new_password = PasswordField('Повторіть пароль', 
                                validators=[DataRequired(message = "Це поле обов'язкове"),
                                        Length(min=6, message='Пароль мусить мати не менше 6 символів'),
                                        EqualTo('new_password')])

    def validate_old_password(self, field):
        if not check_password_hash(current_user.password, field.data):
            raise ValidationError('Це не ваш пароль')