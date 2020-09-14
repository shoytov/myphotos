from flask_security import login_user
from models import User


class UserLogin(object):
	"""
	логин пользователя
	"""
	username = None
	password = None
	
	def __init__(self, username, password):
		self.username = username
		self.password = password
		
	def login(self) -> bool:
		try:
			user = User.authenticate(self.username, self.password)
			login_user(user)
			return True
		except Exception:
			return False
