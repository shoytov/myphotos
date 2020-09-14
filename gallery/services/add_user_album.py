from flask_security import current_user
from models import Album

class AddUserAlbum(object):
	"""
	добавление нового альбома пользователем
	"""
	name = ''
	description = ''
	
	def __init__(self, name, description):
		self.name = name
		self.description = description
		
	def add(self) -> None:
		album = Album()
		album.user = current_user.id
		album.name = self.name
		album.description = self.description
		album.save()
