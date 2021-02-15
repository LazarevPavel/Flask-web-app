#Импорты
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

#_---------------------------------------------------------

#Инициализируем Фласк-приложение
app = Flask(__name__)

#Секретный ключ, защищающий приложение от изменений cookies злоумышленныиками
app.config['SECRET_KEY'] = 'PAVEL'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  #указание SQLA пути до файла базы данных

db = SQLAlchemy(app)  #инициализируем ORM

bcrypt = Bcrypt(app) #инииализируем hash-шифровальщик

login_manager = LoginManager(app) #инициализация менеджера авторизации
login_manager.login_view = 'login' #указываем эндпоинт для авторизации. Туда будет пересылаться пользователь при попытке зайти на эндпоинт, требуещий авторизованного юзера
login_manager.login_message_category = 'info'

#импортируем эндпоинты после инициализации Фласк-приложения
from Flaskblog import routes