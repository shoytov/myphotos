import os
from flask_security import current_user

from config import Config
from models import Album

class DeletePhoto(object):
	"""
	удаление фотографии пользователем
	"""
	album_id = ''
	file = ''
	
	def __init__(self, album_id: str, file: str):
		self.album_id = album_id
		self.file = file
		
	def delete(self) -> str:
		album = Album.objects(id=self.album_id, user=current_user.id)
		
		if album.first():
			album.update_one(__raw__={'$pull': {'photos': {'file': self.file}}})
			album = album.first()
			
			path_max = os.path.join(Config.UPLOADS_DEFAULT_DEST, str(current_user.id), album.slug, self.file)
			path_min = os.path.join(Config.DEFAULT_MIN_DIR, str(current_user.id), album.slug, self.file)
			
			try:
				os.remove(path_max)
				os.remove(path_min)
			except FileNotFoundError:
				pass
			
			return album.slug
		else:
			return ''
