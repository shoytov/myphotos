from flask_security import current_user

from models import Album


class ViewAlbum(object):
	"""
	вывод альбома пользователя по slug
	"""
	slug = ''
	
	def __init__(self, slug):
		self.slug = slug
		
	def album(self):
		album = Album.objects(user=current_user.id, slug=self.slug).first()
		return album