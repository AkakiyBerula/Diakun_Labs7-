from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField, BooleanField
from wtforms.validators import Length, DataRequired, InputRequired
from flask_wtf.file import FileField, FileAllowed


class PostsForm(FlaskForm):
    title = StringField('Введіть заголовок поста', validators=[InputRequired(), Length(min=2, max=80)])
    text = TextAreaField('Введіть текст поста', validators=[Length(max=2500)])
    picture = FileField('Зображення поста', validators=[FileAllowed(['jpg', 'png'])])
    type = SelectField('Оберіть тип категорії', choices=[('News', 'News'), ('Publication', 'Publication'), ('Other', 'Other')])
    enabled = BooleanField('Enabled')
    submit = SubmitField('Підтвердити')