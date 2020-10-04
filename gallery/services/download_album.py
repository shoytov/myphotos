import os
import zipstream
from flask_security import current_user
from flask import Response, stream_with_context
from config import Config
from models import Album


class DownloadAlbum(object):
	"""
	скачивание альбома в zip архиве
	"""
	def __init__(self, album_id: str):
		self.album = Album.objects(id=album_id, user=current_user.id).first()
		
	def generate_zip(self):
		"""
		создание архива в поток
		"""
		path = os.path.join(Config.PHOTOS_DIR, str(current_user.id), self.album.slug)
		z = zipstream.ZipFile(mode='w', compression=zipstream.ZIP_DEFLATED)
		
		for filename in os.listdir(path):
			z.write(os.path.join(path, filename), arcname='{}/{}'.format(self.album.slug, filename))
			yield from z.flush()
		
		yield from z
		
	def download(self):
		return Response(stream_with_context(self.generate_zip()), mimetype='application/zip')
