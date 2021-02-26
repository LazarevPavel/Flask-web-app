from flask import Blueprint

from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import current_user, login_required

from Flaskblog import db
from Flaskblog.models import Post

from .forms import PostForm


#--------------------------------------------


#привязываем систему рутинга по именам. Эта система содержит эндпоинты для постов
posts = Blueprint('posts', __name__)



#Эндпоинт для добавления новых постов
@posts.route("/post/new", methods=['GET', 'POST'])
@login_required  #требуется авторизация
def new_post():
    form = PostForm()   #обозначили форму
    if form.validate_on_submit():   #если нажали на кнопку потдверждения
        post = Post(title=form.title.data, content=form.content.data, author=current_user) #создаём пост
        db.session.add(post)    #добавляем его в базу
        db.session.commit()     #сохраняем
        flash('Your post has been created!', 'success')  #я сделяль
        return redirect(url_for('main.home'))  #перенаправляем домой
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')



#эндпоинт для отображения одного поста
@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id) #находим пост в базе по айди
    return render_template('post.html', title=post.title, post=post)  #показываем



#эндпоинт для обновления поста
@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
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
        return redirect(url_for('posts.post', post_id=post.id))  #перенаправляем на обновлённый пост

    elif request.method == 'GET':  #если это было простое обращение к странице
        form.title.data = post.title    #делаем вид, будто бы юзер начал редактировать свой пост
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post') #готово



#эндпоинт для удаления поста
@posts.route("/post/<int:post_id>/delete", methods=['POST'])  #принимает только запросы POST
@login_required   #требуется авторизация
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)  # находим пост по айди
    if post.author != current_user:   #если запрашивающий не является автором поста
        abort(403)   #пусть идёт лесом
    db.session.delete(post)  #иначе удаляем пост из базы
    db.session.commit()      #сохраняем изменения
    flash('Yout post has been deleted!', 'success')  # сигналим
    return redirect(url_for('main.home'))  #отправляем юзера на домашнюю страницу


