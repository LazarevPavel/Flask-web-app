#Импорты
import secrets
import os
from PIL import Image

from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message

from Flaskblog import app, db, bcrypt, mail
from Flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, RequestResetForm, ResetPasswordForm
from Flaskblog.models import User, Post



#добавляем домашний эндпоинт
@app.route('/')
@app.route('/home')
def home():
    page = request.args.get('page', 1, type=int) #берём номер страницы, на которую нажал юзер (по дефолту будет 1)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5) #берём все посты из базы, сортирем по дате и разделяем их на части (по 5 постов на страницу), потом показываем страницу под номером page
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
        flash('Your account has been updated!', 'success')  #показать табличку "успех"
        return redirect(url_for('account'))  #обновить страницу
    elif request.method == 'GET':
        form.username.data = current_user.username  #вставить в форму юзернэйм
        form.email.data = current_user.email   #вставить в форму эмайл юзера

    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)  #находим аватарку юзера в файлах
    return render_template('account.html', title='Account', image_file=image_file, form=form)  # отправляем юзеру страницу с формой



#Эндпоинт для добавления новых постов
@app.route("/post/new", methods=['GET', 'POST'])
@login_required  #требуется авторизация
def new_post():
    form = PostForm()   #обозначили форму
    if form.validate_on_submit():   #если нажали на кнопку потдверждения
        post = Post(title=form.title.data, content=form.content.data, author=current_user) #создаём пост
        db.session.add(post)    #добавляем его в базу
        db.session.commit()     #сохраняем
        flash('Your post has been created!', 'success')  #я сделяль
        return redirect(url_for('home'))  #перенаправляем домой
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')



#эндпоинт для отображения одного поста
@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id) #находим пост в базе по айди
    return render_template('post.html', title=post.title, post=post)  #показываем



#эндпоинт для обновления поста
@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id) #находим пост по айди
    if post.author != current_user:  #если запрашивающий не является автором статьи
        abort(403)   #то он идёт лесом

    form = PostForm()   #если всё ок, то мы объявляем форму поста

    if form.validate_on_submit():  #если форму уже подтверждили
        post.title = form.title.data    #обновляем форму в бд
        post.content = form.content.data
        db.session.commit()  #запоминаем
        flash('Yout post has been updated!', 'success') #сигналим
        return redirect(url_for('post', post_id=post.id))  #перенаправляем на обновлённый пост

    elif request.method == 'GET':  #если это было простое обращение к странице
        form.title.data = post.title    #делаем вид, будто бы юзер начал редактировать свой пост
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post') #готово



#эндпоинт для удаления поста
@app.route("/post/<int:post_id>/delete", methods=['POST'])  #принимает только запросы POST
@login_required   #требуется авторизация
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)  # находим пост по айди
    if post.author != current_user:   #если запрашивающий не является автором поста
        abort(403)   #пусть идёт лесом
    db.session.delete(post)  #иначе удаляем пост из базы
    db.session.commit()      #сохраняем изменения
    flash('Yout post has been deleted!', 'success')  # сигналим
    return redirect(url_for('home'))  #отправляем юзера на домашнюю страницу



#эндпоинт отображения всех постов указанного пользователя
@app.route('/user/<string:username>')
def user_posts(username):
    page = request.args.get('page', 1, type=int)                   #берём номер страницы, на которую нажал юзер (по дефолту будет 1)
    user = User.query.filter_by(username=username).first_or_404()  #находим пользователя
    posts = Post.query.filter_by(author=user).\
            order_by(Post.date_posted.desc()).\
            paginate(page=page, per_page=5) #берём все посты юзера из базы, сортирем по дате и разделяем их на части (по 5 постов на страницу), потом показываем страницу под номером page
    return render_template('user_posts.html', posts=posts, user=user)  #возвращаем результат работы функции рендера html-шаблона (на выход уйдёт гипертекст)



#отправка подтверждения на почту
def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[user.email])
    msg.body = f'''To reset yout password, visit the following link:
        {url_for('reset_token', token=token, _external=True)}

        If you did not make this request then simply ignore this email and no changes will be made.
    '''
    mail.send(msg)

#эндпоинт запроса на изменение пароля
@app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)



#эндпоинт сброса токена
@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    user = User.verify_reset_token(token)
    if user is None:
        flash('That if an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))

    form = ResetPasswordForm()
    if form.validate_on_submit():  #если введённая информация корректна
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')  #хэшируем пароль пользователя и переводим его в понятный буквенно-цифровой вид
        user.password = hashed_password
        db.session.commit()  #комиттим изменения
        flash(f'Your password has been updated.', 'success')  #выдаём сообщение об успешной регистрации
        return redirect(url_for('login'))  #перенаправляем юзера на домашнюю страницу
    return render_template('reset_token.html', title='Reset Password', form=form)




