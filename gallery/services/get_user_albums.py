from flask_security import current_user
from models import Album


class GetUserAlbums(object):
	"""
	вывод альбомов пользователя
	"""
	@staticmethod
	def get():
		albums = Album.objects(user=current_user.id).order_by('-created')
		return albums