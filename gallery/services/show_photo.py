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
			pipeline = [
				{'$unwind': {'path': '$photos', 'includeArrayIndex': 'counter'}}
			]
			# выбираем конкретно запрашиваемую фотографию
			photo = album.aggregate(*pipeline, {'$match': {'photos.file': self.file}})
			photo = list(photo)[0]
			
			# предыдущая и следующая фотографии в альбоме
			photo_prev = album.aggregate(*pipeline, {'$match': {'counter': photo.get('counter') - 1}})
			photo_next = album.aggregate(*pipeline, {'$match': {'counter': photo.get('counter') + 1}})
		else:
			photo = []
			photo_prev = []
			photo_next = []
	
		try:
			photo_prev = list(photo_prev)[0]
		except IndexError:
			photo_prev = []
			photo_prev.append({'photos': []})
			photo_prev = photo_prev[0]
			
		try:
			photo_next = list(photo_next)[0]
		except IndexError:
			photo_next = []
			photo_next.append({'photos': []})
			photo_next = photo_next[0]
		
		return [photo, photo_prev, photo_next]
