from flask_security import current_user

from models import Album

class FilterByCamera(object):
	"""
	фильтрация фотографий в альбоме по моделе камеры
	"""
	album_slug = ''
	camera = ''
	
	def __init__(self, album_slug, camera):
		self.album_slug = album_slug
		self.camera = camera
		
	def filter(self) -> list:
		photos = []
		album = Album.objects(slug=self.album_slug, user=current_user.id)
		
		if album.first():
			pipelines = [
				{'$unwind': {'path': '$photos', 'includeArrayIndex': 'counter'}},
				{'$match': {'photos.device': self.camera}}
			]
			photos = list(album.aggregate(*pipelines))
			
		return photos
