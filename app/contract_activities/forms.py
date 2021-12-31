from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, FloatField
from wtforms.fields.html5 import DateField
from wtforms.validators import Length, DataRequired, InputRequired, Required, Regexp
from .models import Contractypes


class ContractForm(FlaskForm):
    contract_code = StringField("Шифр договору",validators=[
                        InputRequired(message="Це поле обов'язкове"),
                        Regexp(r'^[A-Z]{3}-[0-9]{4}$', 0,
                        message="Шифр договору повинен складатись з трьох латинських великих літер, дефізу і чотирьох цифр")], )
    organization_name = StringField('Найменування організації', 
                        validators=[InputRequired(message="Це поле обов'язкове"), 
                        Length(max=100, message="Поле має мати не більше ста символів")])
    deadline = DateField('Термін виконання', format="%Y-%m-%d",
                            validators=[Required(message="Це поле обов'язкове")])
    contract_amount = StringField('Cума договору', 
                    validators=[
                    DataRequired(message="Це поле обов'язкове"),
                    Regexp(r'[0-9]*\.[0-9]{2}$', 0,
                    message="Сума повинна мати дробове значення дві цифри після коми")])
    contract_type = SelectField('Оберіть категорію', coerce = int)
    submit = SubmitField('Добавити договір')


class CategoryForm(FlaskForm):
    contract_type = StringField('Ввести тип категорії', validators=[DataRequired(message="Це поле обов'язкове"), Length(min=0, max=40)])
    submit = SubmitField('Виконати')