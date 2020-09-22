from flask_admin.contrib.mongoengine import ModelView
from init import app, admin
from models import User
from gallery.gallery import gallery
from flask import Response, redirect
from init import basic_auth
from filters import my_strftime
from werkzeug.exceptions import HTTPException


class AuthException(HTTPException):
    def __init__(self, message):
        super().__init__(message, Response(
            "You could not be authenticated. Please refresh the page.", 401,
            {'WWW-Authenticate': 'Basic realm="Login Required"'}
        ))
        
        
class ModelView(ModelView):
    def is_accessible(self):
        if not basic_auth.authenticate():
            raise AuthException('Not authenticated.')
        else:
            return True

    def inaccessible_callback(self, name, **kwargs):
        return redirect(basic_auth.challenge())


admin.add_view(ModelView(User, 'Пользователи'))

app.register_blueprint(gallery, url_prefix='')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
