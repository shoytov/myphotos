from typing import List
from math import ceil
from flask_security import current_user

from models import Album
from config import Config


class ViewAlbum(object):
	"""
	вывод альбома пользователя по slug
	"""
	slug = ''
	_album = None
	
	def __init__(self, slug):
		self.slug = slug
		self._album = Album.objects(user=current_user.id, slug=self.slug)
		
	def album(self) -> Album:
		"""
		получение документа альбома
		"""
		return self._album.first()
	
	def photos(self, page:int = 1) -> dict:
		"""
		вывод определенного кол-ва фотографий для пагинации
		"""
		
		# подсчет общего кол-ва страниц
		pages_total = ceil(len(self._album.first().photos) / Config.IMG_PER_PAGE)
		
		# массив с фотографиями для вывода на странице
		page = int(page)
		
		start = (page - 1) * Config.IMG_PER_PAGE
			
		photos = self._album.first().photos[start:start + Config.IMG_PER_PAGE]
		
		result = {
			'pages_total': pages_total,
			'current_page': page,
			'photos': photos
		}
		
		return result

	def get_devices(self) -> List[dict]:
		"""
		получение списка камер, на которые сделаны фотографии в альбоме
		"""
		pipelines = [
			{'$unwind': {'path': '$photos'}},
			{'$group': {'_id': '$photos.device'}}
		]
		
		devices = list(self._album.aggregate(*pipelines))
		return devices
