from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required

from Flaskblog import db, bcrypt
from Flaskblog.models import User, Post

from .forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from .utils import save_picture, send_reset_email


#-----------------------------------------------


#привязываем систему рутинга по объектам. Эта система содержит в себе эндпоинты для юзера
users = Blueprint('users', __name__)


#добавляем эндпоинт регистрации юзера
@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:  #если пользователь уже авторизован
        return redirect(url_for('main.home'))   #нет смысла регистрировать его снова, перенаправляем на домашнюю страницу

    form = RegistrationForm() #создаём экземпляр регистрационной формы
    if form.validate_on_submit():  #если введённая информация корректна
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')  #хэшируем пароль пользователя и переводим его в понятный буквенно-цифровой вид
        user = User(username=form.username.data, email=form.email.data, password=hashed_password) #создаём юзера с данными из формы (но с шифрованным паролем)
        db.session.add(user) #добавляем нового пользователя в БД
        db.session.commit()  #комиттим изменения
        flash(f'Account created for {form.username.data}!', 'success')  #выдаём сообщение об успешной регистрации
        return redirect(url_for('users.login'))  #перенаправляем юзера на домашнюю страницу
    return render_template('register.html', title='Register', form=form) #отправляем юзеру страницу с формой регистрации



#добавляем эндпоинт авторизации юзера
@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:  # если пользователь уже авторизован
        return redirect(url_for('main.home'))  # нет смысла авторизовываться снова, перенаправляем на домашнюю страницу

    form = LoginForm() #создаём экземпляр авторизационной формы
    if form.validate_on_submit():  # если введённая информация корректна
        user = User.query.filter_by(email=form.email.data).first()  #ищем пользователя
        if user and bcrypt.check_password_hash(user.password, form.password.data):  #если залогинилиись норм
            login_user(user, remember=form.remember.data)   #функция логининга юзера
            next_page = request.args.get('next') #берём адрес следующей страницы после авторизации
            return redirect(next_page) if next_page else redirect(url_for('main.home'))  #перенаправляем на следующую страницу или на домашнюю страницу, если следующей нет
        else:
            flash('Login Unsuccessful. Please check email and password.', 'danger') #выкидываем сообщение
    return render_template('login.html', title='Login', form=form) #отправляем юзеру страницу с формой авторизации



#ендпоинт для разлогинивания юзера
@users.route('/logout')
def logout():
    logout_user()  #функция разлогинивания
    return redirect(url_for('main.home'))  #перенаправляем на домашнюю страницу



#Энпоинт для входа на страницу аккаунта
@users.route('/account', methods=['GET', 'POST'])
@login_required  #требуется авторизация
def account():
    form = UpdateAccountForm() #создаём форму, чтобы отобразить её на странице аккаунта
    if form.validate_on_submit():  #по нажатию на кнопку
        if form.picture.data: #если хотят залить аватарку новую
            picture_file = save_picture(form.picture.data) #сохраняем новую картинку
            current_user.image_file = picture_file         #меняем картинку пользователя в данных
        current_user.username = form.username.data  #поменять юзернэйм
        current_user.email = form.email.data  #поменять эмайл
        db.session.commit()  #закрепить измененния
        flash('Your account has been updated!', 'success')  #показать табличку "успех"
        return redirect(url_for('users.account'))  #обновить страницу
    elif request.method == 'GET':
        form.username.data = current_user.username  #вставить в форму юзернэйм
        form.email.data = current_user.email   #вставить в форму эмайл юзера

    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)  #находим аватарку юзера в файлах
    return render_template('account.html', title='Account', image_file=image_file, form=form)  # отправляем юзеру страницу с формой



#эндпоинт отображения всех постов указанного пользователя
@users.route('/user/<string:username>')
def user_posts(username):
    page = request.args.get('page', 1, type=int)                   #берём номер страницы, на которую нажал юзер (по дефолту будет 1)
    user = User.query.filter_by(username=username).first_or_404()  #находим пользователя
    posts = Post.query.filter_by(author=user).\
            order_by(Post.date_posted.desc()).\
            paginate(page=page, per_page=5) #берём все посты юзера из базы, сортирем по дате и разделяем их на части (по 5 постов на страницу), потом показываем страницу под номером page
    return render_template('user_posts.html', posts=posts, user=user)  #возвращаем результат работы функции рендера html-шаблона (на выход уйдёт гипертекст)



#эндпоинт запроса на изменение пароля
@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)



#эндпоинт сброса токена
@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))

    form = ResetPasswordForm()
    if form.validate_on_submit():  #если введённая информация корректна
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')  #хэшируем пароль пользователя и переводим его в понятный буквенно-цифровой вид
        user.password = hashed_password
        db.session.commit()  #комиттим изменения
        flash(f'Your password has been updated.', 'success')  #выдаём сообщение об успешной регистрации
        return redirect(url_for('users.login'))  #перенаправляем юзера на домашнюю страницу
    return render_template('reset_token.html', title='Reset Password', form=form)



