from flask_security import current_user

from models import Album

class ShowPhoto(object):
	"""
	вывод оригинала фотографии
	"""
	album_id = ''
	file = ''
	
	def __init__(self, album_id: str, file: str):
		self.album_id = album_id
		self.file = file
		
	def show(self) -> list:
		album = Album.objects(id=self.album_id, user=current_user.id, photos__file=self.file)
		
		if album.first():
			pipelines = [
				{'$unwind': {'path': '$photos'}},
				{'$match': {'photos.file': self.file}}
			]
			photo = album.aggregate(*pipelines)
		else:
			photo = []
		
		try:
			return list(photo)[0]
		except IndexError:
			photo.append({'photos': []})
			return photo[0]
