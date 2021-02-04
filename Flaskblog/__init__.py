#Импорты
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#_---------------------------------------------------------

#Инициализируем Фласк-приложение
app = Flask(__name__)

#Секретный ключ, защищающий приложение от изменений cookies злоумышленныиками
app.config['SECRET_KEY'] = 'PAVEL'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  #указание SQLA пути до файла базы данных

db = SQLAlchemy(app)  #инициализируем ORM


from Flaskblog import routes