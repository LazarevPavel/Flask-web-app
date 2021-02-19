#импорты
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed

from flask_login import current_user

from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from Flaskblog.models import User


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


    #проверка существования юзера с указанным именем
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()  #ищем юзера с указанным именем
        if user:   #если такой юзер есть, выкинем ошибку
            raise ValidationError('That username is taken. Please choose a different one.')


    # проверка существования почты
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()  # ищем юзера с указанным именем
        if user:  # если такой юзер есть, выкинем ошибку
            raise ValidationError('That email is taken. Please choose a different one.')





#Класс формы обновления информации аккаунта (наследуется от FlaskForm)
class UpdateAccountForm(FlaskForm):
    #поле: имя юзера типа String, не может быть пустым (DataRequired), длина имени должна находиться в пределах 2-20 символов (Length)
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    #поле: почта типа String, не может быть пустым (DataRequired), соблюдается контроль написания адреса почты (Email)
    email = StringField('Email', validators=[DataRequired(), Email()])
    #поле: картинка
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])

    #кнопка подтверждения
    submit = SubmitField('Update')


    #проверка существования юзера с указанным именем
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()  #ищем юзера с указанным именем
            if user:   #если такой юзер есть, выкинем ошибку
                raise ValidationError('That username is taken. Please choose a different one.')


    # проверка существования юзера с указанным именем
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()  # ищем юзера с указанным именем
            if user:  # если такой юзер есть, выкинем ошибку
                raise ValidationError('That email is taken. Please choose a different one.')





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



#Класс формы для создания постов
class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])  #поле: заголовок поста
    content = TextAreaField('Content', validators=[DataRequired()])  #поле: контент поста
    submit = SubmitField('Post')   #кнопка "запостить"


#форма входа на страницу сброса пароля
class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    # проверка существования почты
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()  # ищем юзера с указанной почтой
        if user is None:  # если такой юзер есть, выкинем ошибку
            raise ValidationError('There is no account with that email. You must register first.')


#форма сброса пароля на новый
class ResetPasswordForm(FlaskForm):
    # поле: пароль типа Password, не может быть пустым
    password = PasswordField('Password', validators=[DataRequired()])
    # поле: повтором пароля типа Password, не может быть пустым, проводится проверка соответствия паролей, введённых в оба поля
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

