import os
import io
from flask_security import current_user
from flask import send_file
from PIL import Image as PilImage
import PIL

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
			'max': Config.UPLOADS_DEFAULT_DEST,
			'full': Config.UPLOADS_DEFAULT_DEST
		}

		if album:
			file = os.path.join(case.get(self.filetype), str(current_user.id), album.slug, self.filename)
			
			# ресайз картинки
			if self.filetype == 'max':
				img = PilImage.open(file, mode='r')
				ratio = (Config.MAX_WIDTH / float(img.size[0]))
				height = int((float(img.size[1]) * float(ratio)))
				img = img.resize((Config.MAX_WIDTH, height), PIL.Image.ANTIALIAS)
				rgb_im = img.convert('RGB')
				
				img_response = io.BytesIO()
				rgb_im.save(img_response, 'JPEG')
				img_response.seek(0)
			else:
				img_response = file
		else:
			img_response = os.path.join(Config.BASE_DIR, 'static/images/forbidden.jpg')
		
		if self.filetype != 'full':
			as_attachment = False
		else:
			as_attachment = True
			
		return send_file(img_response, mimetype='image/jpeg', as_attachment=as_attachment)
