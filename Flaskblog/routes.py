#Импорты
import secrets
import os
from PIL import Image

from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required

from Flaskblog import app, db, bcrypt
from Flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm
from Flaskblog.models import User, Post


#информация, хранящаяся в памяти
posts = [
    {
        'author': 'Pavel Lazarev',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Pavel Anreev',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'June 23, 2018'
    }
]



#добавляем домашний эндпоинт
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts=posts)  #возвращаем результат работы функции рендера html-шаблона (на выход уйдёт гипертекст)


#добавляем about эндпоинт
@app.route('/about')
def about():
    return render_template('about.html', title='About') #возвращаем отрендеренный html-шаблон


#добавляем эндпоинт регистрации юзера
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:  #если пользователь уже авторизован
        return redirect(url_for('home'))   #нет смысла регистрировать его снова, перенаправляем на домашнюю страницу

    form = RegistrationForm() #создаём экземпляр регистрационной формы
    if form.validate_on_submit():  #если введённая информация корректна
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')  #хэшируем пароль пользователя и переводим его в понятный буквенно-цифровой вид
        user = User(username=form.username.data, email=form.email.data, password=hashed_password) #создаём юзера с данными из формы (но с шифрованным паролем)
        db.session.add(user) #добавляем нового пользователя в БД
        db.session.commit()  #комиттим изменения
        flash(f'Account created for {form.username.data}!', 'success')  #выдаём сообщение об успешной регистрации
        return redirect(url_for('login'))  #перенаправляем юзера на домашнюю страницу
    return render_template('register.html', title='Register', form=form) #отправляем юзеру страницу с формой регистрации


#добавляем эндпоинт авторизации юзера
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:  # если пользователь уже авторизован
        return redirect(url_for('home'))  # нет смысла авторизовываться снова, перенаправляем на домашнюю страницу

    form = LoginForm() #создаём экземпляр авторизационной формы
    if form.validate_on_submit():  # если введённая информация корректна
        user = User.query.filter_by(email=form.email.data).first()  #ищем пользователя
        if user and bcrypt.check_password_hash(user.password, form.password.data):  #если залогинилиись норм
            login_user(user, remember=form.remember.data)   #функция логининга юзера
            next_page = request.args.get('next') #берём адрес следующей страницы после авторизации
            return redirect(next_page) if next_page else redirect(url_for('home'))  #перенаправляем на следующую страницу или на домашнюю страницу, если следующей нет
        else:
            flash('Login Unsuccessful. Please check email and password.', 'danger') #выкидываем сообщение
    return render_template('login.html', title='Login', form=form) #отправляем юзеру страницу с формой авторизации


#ендпоинт для разлогинивания юзера
@app.route('/logout')
def logout():
    logout_user()  #функция разлогинивания
    return redirect(url_for('home'))  #перенаправляем на домашнюю страницу



#функция сохранения картинки
def save_picture(form_picture):
    random_hex = secrets.token_hex(8) #генерация 8 символов шестнадцатиричной системы счисления
    _, t_ext = os.path.splitext(form_picture.filename) #разделить имя файла на имя и расширение
    picture_fn = random_hex + t_ext  #соединяем кодировку и расширение
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn) #создаём строку-путь до картинки
    output_size = (125, 125)  #обозначаем размер картинки
    img = Image.open(form_picture)  #открываем картинку, заданную юзеру
    img.thumbnail(output_size)  #уменьшаем заданную картинку до обозначенных размеров
    img.save(picture_path) #сохраняем картинку согласно пути
    return picture_fn #возвращаем название файла-картинки



#Энпоинт для входа на страницу аккаунта
@app.route('/account', methods=['GET', 'POST'])
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
        flash('Yout account has been updated!', 'success')  #показать табличку "успех"
        return redirect(url_for('account'))  #обновить страницу
    elif request.method == 'GET':
        form.username.data = current_user.username  #вставить в форму юзернэйм
        form.email.data = current_user.email   #вставить в форму эмайл юзера

    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)  #находим аватарку юзера в файлах
    return render_template('account.html', title='Account', image_file=image_file, form=form)  # отправляем юзеру страницу с формой
