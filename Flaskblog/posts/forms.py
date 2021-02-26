#импорты
from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired



#Класс формы для создания постов
class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])  #поле: заголовок поста
    content = TextAreaField('Content', validators=[DataRequired()])  #поле: контент поста
    submit = SubmitField('Post')   #кнопка "запостить"