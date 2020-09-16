from typing import List
from flask_security import current_user

from models import Album


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
