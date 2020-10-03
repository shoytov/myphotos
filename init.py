from flask import Flask, request, session
from flask_mongoengine import MongoEngine
from flask_session import Session
from flask_babelex import Babel
from flask_login import LoginManager
from flask_admin import Admin
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_basicauth import BasicAuth

from config import Config

app = Flask(__name__)

app.config.from_object(Config)

db = MongoEngine()
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

# локализация
babel = Babel(app)

basic_auth = BasicAuth(app)

SESSION_TYPE = 'mongodb'
SESSION_MONGODB_DB = Config.MONGODB_SETTINGS.get('db')
app.config.from_object(__name__)
Session(app)

admin = Admin(app, name='admin', template_mode='bootstrap3')


@babel.localeselector
def get_locale():
	if request.args.get('lang'):
		session['lang'] = request.args.get('lang')
	return session.get('lang', 'ru')
