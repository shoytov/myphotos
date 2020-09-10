from flask import Flask, request, session
from flask_mongoengine import MongoEngine
from flask_session import Session
from flask_babelex import Babel

from config import Config

app = Flask(__name__)

app.config.from_object(Config)

db = MongoEngine(app)

# локализация
babel = Babel(app)

SESSION_TYPE = 'mongodb'
SESSION_MONGODB_DB = Config.MONGODB_SETTINGS.get('db')
app.config.from_object(__name__)
Session(app)


@babel.localeselector
def get_locale():
	if request.args.get('lang'):
		session['lang'] = request.args.get('lang')
	return session.get('lang', 'ru')
