from flask_security import current_user


class CheckUserLogin(object):
	"""
	проверка на залониненного пользователя
	"""
	@staticmethod
	def check() -> bool:
		if not current_user.is_authenticated:
			return False
		else:
			return True
