from flask_admin.contrib.mongoengine import ModelView
from init import app, admin
from models import User
from gallery.gallery import gallery
from filters import my_strftime


admin.add_view(ModelView(User, 'Пользователи'))

app.register_blueprint(gallery, url_prefix='')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)