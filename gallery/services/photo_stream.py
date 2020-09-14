from flask_security import current_user

from models import Album


class PhotoStream(object):
	"""
	фотопоток для пользователя
	"""
	@staticmethod
	def stream() -> list:
		pipeline = [
			{'$unwind': {'path': '$photos'}},
			{'$sort': {'photos.created': -1}},
			{'$limit': 100}
		]
		photos = Album.objects(user=current_user.id).aggregate(*pipeline)

		return list(photos)
