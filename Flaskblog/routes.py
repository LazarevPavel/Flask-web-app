#Импорты
from flask import render_template, url_for, flash, redirect

from Flaskblog import app
from Flaskblog.forms import RegistrationForm, LoginForm
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
    form = RegistrationForm() #создаём экземпляр регистрационной формы
    if form.validate_on_submit():  #если введённая информация корректна
        flash(f'Account created for {form.username.data}!', 'success')  #выдаём сообщение об успешной регистрации
        return redirect(url_for('home'))  #перенаправляем юзера на домашнюю страницу
    return render_template('register.html', title='Register', form=form) #отправляем юзеру страницу с формой регистрации


#добавляем эндпоинт авторизации юзера
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm() #создаём экземпляр авторизационной формы
    if form.validate_on_submit():  # если введённая информация корректна
        if form.email.data == 'admin@blog.com' and form.password.data == 'password': #Если авторизация прошла успешно
            flash('You have been logged in!', 'success')  #выкидываем сообщение
            return redirect(url_for('home'))            #перенаправляем юзера на домашнюю страницу
        else:  #если авторизация провалилась
            flash('Login Unsuccessful. Please check username and password.', 'danger') #выкидываем сообщение
    return render_template('login.html', title='Login', form=form) #отправляем юзеру страницу с формой авторизации
