from math import ceil
from flask_security import current_user

from models import Album
from config import Config


class PhotoStream(object):
	"""
	фотопоток для пользователя
	"""
	@staticmethod
	def stream(page) -> dict:
		pipeline = [
			{'$unwind': {'path': '$photos'}},
			{'$sort': {'photos.created': -1}},
			{'$skip': (page - 1) * Config.IMG_PER_PAGE},
			{'$limit': Config.IMG_PER_PAGE}
		]
		photos = Album.objects(user=current_user.id).aggregate(*pipeline)
		
		# подсчет кол-ва страниц для пагинации
		pipeline = [
			{'$unwind': {'path': '$photos'}},
			{'$count': 'total'}
		]
		photos_total = Album.objects(user=current_user.id).aggregate(*pipeline)
		pages_total = ceil(int(list(photos_total)[0].get('total', 1)) / Config.IMG_PER_PAGE)

		result = {
			'photos': list(photos),
			'pages_total': pages_total,
			'current_page': page,
		}
		return result
