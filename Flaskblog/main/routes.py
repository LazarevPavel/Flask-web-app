from flask import Blueprint
from flask import render_template, request

from Flaskblog.models import Post

#------------------------------------------


#привязываем систему рутинга по именам. Эта система содержит эндпоинты для постов
main = Blueprint('main', __name__)



#добавляем домашний эндпоинт
@main.route('/')
@main.route('/home')
def home():
    page = request.args.get('page', 1, type=int) #берём номер страницы, на которую нажал юзер (по дефолту будет 1)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5) #берём все посты из базы, сортирем по дате и разделяем их на части (по 5 постов на страницу), потом показываем страницу под номером page
    return render_template('home.html', posts=posts)  #возвращаем результат работы функции рендера html-шаблона (на выход уйдёт гипертекст)



#добавляем about эндпоинт
@main.route('/about')
def about():
    return render_template('about.html', title='About') #возвращаем отрендеренный html-шаблон
