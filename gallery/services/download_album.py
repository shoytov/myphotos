import os
from io import BytesIO
import zipfile
from flask_security import current_user
from flask import send_file
from config import Config
from models import Album


class DownloadAlbum(object):
	"""
	скачивание альбома в zip архиве
	"""
	def __init__(self, album_id: str):
		self.album = Album.objects(id=album_id, user=current_user.id).first()
		
	def download(self):
		memory_file = BytesIO()
		path = os.path.join(Config.PHOTOS_DIR, str(current_user.id), self.album.slug)
		
		with zipfile.ZipFile(memory_file, 'w') as zf:
			for root, dirs, files in os.walk(path):
				for file in files:
					zf.write(os.path.join(path, file), '{}/{}'.format(self.album.slug, file), zipfile.ZIP_DEFLATED)
		
		memory_file.seek(0)
		
		return send_file(memory_file, attachment_filename='{}.zip'.format(self.album.slug), as_attachment=True)
