#Импорты
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

from Flaskblog.config import Config

#_---------------------------------------------------------

db = SQLAlchemy()  #инициализируем ORM

bcrypt = Bcrypt() #инииализируем hash-шифровальщик

login_manager = LoginManager() #инициализация менеджера авторизации
login_manager.login_view = 'users.login' #указываем эндпоинт для авторизации. Туда будет пересылаться пользователь при попытке зайти на эндпоинт, требуещий авторизованного юзера
login_manager.login_message_category = 'info'

mail = Mail() #инициализируем почтового системы почты

#--------------------------

#функция для инициализации приложения с различными конфигурациями
def create_app(config_class=Config):

    # Инициализируем Фласк-приложение
    app = Flask(__name__)
    app.config.from_object(Config)  # считывание параметров конфигурации из класса конфигурации Config

    #коннектим модули с нашим приложением
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    # импортируем эндпоинты после инициализации Фласк-приложения
    from Flaskblog.main.routes import main
    from Flaskblog.users.routes import users
    from Flaskblog.posts.routes import posts
    from Flaskblog.errors.handlers import errors
    # регистрируем в приложении созданные блупринты
    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(errors)

    return app


