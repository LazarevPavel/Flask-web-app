import secrets
import os
from PIL import Image

from flask import url_for, current_app
from flask_mail import Message

from Flaskblog import mail

#----------------------------------------------

#функция сохранения картинки
def save_picture(form_picture):
    random_hex = secrets.token_hex(8) #генерация 8 символов шестнадцатиричной системы счисления
    _, t_ext = os.path.splitext(form_picture.filename) #разделить имя файла на имя и расширение
    picture_fn = random_hex + t_ext  #соединяем кодировку и расширение
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn) #создаём строку-путь до картинки
    output_size = (125, 125)  #обозначаем размер картинки
    img = Image.open(form_picture)  #открываем картинку, заданную юзеру
    img.thumbnail(output_size)  #уменьшаем заданную картинку до обозначенных размеров
    img.save(picture_path) #сохраняем картинку согласно пути
    return picture_fn #возвращаем название файла-картинки



#отправка подтверждения на почту
def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[user.email])
    msg.body = f'''To reset yout password, visit the following link:
        {url_for('users.reset_token', token=token, _external=True)}

        If you did not make this request then simply ignore this email and no changes will be made.
    '''
    mail.send(msg)