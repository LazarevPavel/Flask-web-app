from flask import Blueprint, render_template


#привязываем систему рутинга по объектам. Эта система содержит в себе эндпоинты для страниц ошибок
errors = Blueprint('errors', __name__)



#обработка ошибки 404
@errors.app_errorhandler(404)
def error_404(error):
    return render_template('errors/404.html'), 404


#обработка ошибки 403
@errors.app_errorhandler(403)
def error_403(error):
    return render_template('errors/403.html'), 403


#обработка ошибки 500
@errors.app_errorhandler(500)
def error_500(error):
    return render_template('errors/404.html'), 500