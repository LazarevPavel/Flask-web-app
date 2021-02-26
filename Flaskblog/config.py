

class Config:
    # Секретный ключ, защищающий приложение от изменений cookies злоумышленныиками
    SECRET_KEY = 'PAVEL'    #os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'  # указание SQLA пути до файла базы данных  #os.environ.get('SQLALCHEMY_DATABASE_URI')

    # указываем данные для работы с почтой
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'kymarimka@gmail.com'  #os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = 'kymarimkaLOL'    #os.environ.get('EMAIL_PASS')