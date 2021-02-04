#импорты
from Flaskblog import db
from datetime import datetime


#Класс модели юзера
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)    #ID юзера - первичный ключ
    username = db.Column(db.String(20), unique=True, nullable=False)    #имя юзера длины 20 или меньше, уникальное, не пустое
    email = db.Column(db.String(120), unique=True, nullable=False)      #имя юзера длины 20 или меньше, уникальное, не пустое
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')   #аватарка юзера, не пустая, есть дефолтная картинка, если у юзера нет своей
    password = db.Column(db.String(60), nullable=False)  #пароль юзера, не пустое
    posts = db.relationship('Post', backref='author', lazy=True) #связь постов и юзеров. добавление столбца Post, в постах добавляем столбец author

    #магический метод форматного вывода объекта класса
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


#Класс поста в блоге
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # ID юзера - первичный ключ
    title = db.Column(db.String(100), nullable=False) #заголовок, не пустой
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) #дата размещения поста, не пустое, по дефолту ставится настоящий момент времени
    content = db.Column(db.Text, nullable=False)    #контент поста текстового типа, не пустой
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) #ссылка на автора поста

    #магический метод форматного вывода поста
    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"




# ----------------------------------------------------------
#ручное добавление данных в БД (для проверки работы)
'''
db.create_all()  #создать все таблицы

# Пробная попытка добавить пользователя
user_1 = User(username='Pavel', email='j@gmail.com', password='password')
db.session.add(user_1)

# пробная попытка добавить пост
post_1 = Post(title='Blog Post 1', content='First Post Content!', user_id='1')
post_2 = Post(title='Blog Post 2', content='Second Post Content!', user_id='1')
db.session.add(post_1)
db.session.add(post_2)
db.session.commit()


# проверка результата
print(User.query.filter_by(username='Pavel').first().posts)
'''

# _-----------------------------------------------------------