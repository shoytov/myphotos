import os
import shutil
from flask_security import current_user

from config import Config
from models import Album


class DeleteAlbum(object):
	"""
	удаление альбома пользователя со всеми фотографиями
	"""
	album_id = ''
	
	def __init__(self, album_id):
		self.album_id = album_id
		
	def delete(self) -> None:
		album = Album.objects(id=self.album_id, user=current_user.id).first()
		
		if album:
			path = os.path.join(Config.UPLOADS_DEFAULT_DEST, str(current_user.id), album.slug)
			
			try:
				shutil.rmtree(path)
			except FileNotFoundError:
				pass
			
			album.delete()
