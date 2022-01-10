from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import ValidationError, InputRequired, Length, AnyOf
from flask_wtf import FlaskForm
from re import match
from email_validator import validate_email, EmailSyntaxError

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired('A username is required!'), 
                            Length(min=5, max=10, message='Must be from 5 to 10 symbols')])
    password = PasswordField('password', validators=[InputRequired('Password is required!'), 
                            AnyOf(values=['password', 'secret'])])


class RegistrationForm(FlaskForm):
    login = StringField("Логін (адреса електронної пошти)*")
    password = PasswordField("Пароль *")
    confirm_password = PasswordField("Підтвердження паролю")
    number = StringField("Номер *")
    pin = StringField("Пін *")
    year = SelectField("Рік *", choices=range(1980, 2022))
    diplom_serial = StringField("Серія")
    diplom_number = StringField("Номер *")
    submit = SubmitField("Зареєструвати")

    def validate_login(self, login):
        user_login = self.login.data
        if user_login is None:
            raise ValidationError("Це поле має бути обов'язкове")
        else:
            try:
                validate_email(user_login)
            except EmailSyntaxError:
                raise ValidationError("Неправильно введена електронна пошта!")


    def validate_password(self, password):
        user_password = self.password.data
        if user_password is None:
            raise ValidationError("Це поле має бути обов'язкове")
        elif len(user_password) < 6:
            raise ValidationError("Пароль мусить бути не менше 6 символів")

    def validate_confirm_password(self, confirm_password):
        if self.confirm_password.data is None:
            raise ValidationError("Це поле має бути обов'язкове")
        elif self.password.data != self.confirm_password.data:
            raise ValidationError("Паролі не співпадають")

    def validate_number(self, number):
        user_num = self.number.data
        if match(r"^[0-9]{7}$", user_num) is None:
            raise ValidationError("Поле повинно містити строго 7 цифр")
        elif user_num is None:
            raise ValidationError("Це поле має бути обов'язкове")

    def validate_pin(self, pin):
        user_pin = self.pin.data
        if match(r"^[0-9]{4}$", user_pin) is None:
            raise ValidationError("Поле повинно містити строго 4 цифр")
        elif user_pin is None:
            raise ValidationError("Це поле має бути обов'язкове")

    def validate_diplom_serial(self, diplom_serial):
        user_diplom_serial = self.diplom_serial.data
        if self.year.data < "2015":
            if match(r"^[A-Z]{2}$", user_diplom_serial) is None:
                raise ValidationError("Серія диплому повинна складатись з двох латинських літер!")
        else:
            if match(r"^[A-Z]{1}[0-9]{2}$", user_diplom_serial) is None:
                raise ValidationError("Серія диплому повинна складатись з однієї латинських літер та двох цифр!")

    def validate_diplom_number(self, diplom_number):
        user_diplom_number = self.diplom_number.data
        if self.year.data < "2015":
            if match(r"^[0-9]{8}$", user_diplom_number) is None:
                raise ValidationError("Номер диплому повинен складатись з 8 цифр!")
            elif user_diplom_number is None:
                raise ValidationError("Це поле має бути обов'язкове")
        else:
            if match(r"^[0-9]{6}$", user_diplom_number) is None:
                raise ValidationError("Номер диплому повинен складатись з 6 цифр!")
            elif user_diplom_number is None:
                raise ValidationError("Це поле має бути обов'язкове")
    


