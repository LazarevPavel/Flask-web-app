#импорты
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo


#Класс регистрационной формы (наследуется от FlaskForm)
class RegistrationForm(FlaskForm):
    #поле: имя юзера типа String, не может быть пустым (DataRequired), длина имени должна находиться в пределах 2-20 символов (Length)
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    #поле: почта типа String, не может быть пустым (DataRequired), соблюдается контроль написания адреса почты (Email)
    email = StringField('Email', validators=[DataRequired(), Email()])
    #поле: пароль типа Password, не может быть пустым
    password = PasswordField('Password', validators=[DataRequired()])
    #поле: повтором пароля типа Password, не может быть пустым, проводится проверка соответствия паролей, введённых в оба поля
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    #кнопка подтверждения
    submit = SubmitField('Sign Up')




#Класс авторизационной формы (наследуется от FlaskForm)
class LoginForm(FlaskForm):
    #поле: почта типа String, не может быть пустым (DataRequired), соблюдается контроль написания адреса почты (Email)
    email = StringField('Email', validators=[DataRequired(), Email()])
    #поле: пароль типа Password, не может быть пустым
    password = PasswordField('Password', validators=[DataRequired()])
    #Галочка "запомить меня"
    remember = BooleanField('Remember me')
    #кнопка подтверждения
    submit = SubmitField('Login')