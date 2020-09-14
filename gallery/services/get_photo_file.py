import os
from flask_security import current_user
from flask import send_file

from config import Config
from models import Album


class GetPhotoFile(object):
	"""
	получение файла
	"""
	album_id = ''
	filename = ''
	filetype = ''
	
	def __init__(self, album_id: str, filename: str, filetype: str):
		self.album_id = album_id
		self.filename = filename
		self.filetype = filetype
		
	def get(self):
		album = Album.objects(id=self.album_id, user=current_user.id).first()
		
		case = {
			'min': Config.MIN_PHOTOS_DIR,
			'max': Config.UPLOADS_DEFAULT_DEST
		}

		if album:
			file = os.path.join(case.get(self.filetype), str(current_user.id), album.slug, self.filename)
		else:
			file = os.path.join(Config.BASE_DIR, 'static/images/forbidden.jpg')
			
		return send_file(file, mimetype='image/jpeg')
