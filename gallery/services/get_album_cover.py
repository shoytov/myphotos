import os
import io
from flask import send_file
from flask_security import current_user
from PIL import Image as PilImage
import PIL

from config import Config
from models import Album


class GetAlbumCover(object):
	"""
	получение картинки для обложки альбома
	"""
	album_id = ''
	
	def __init__(self, album_id):
		self.album_id = album_id
		
	def cover(self):
		album = Album.objects(id=self.album_id, user=current_user.id).first()
		
		try:
			photo = album.photos[0]
			photo_path = os.path.join(Config.UPLOADS_DEFAULT_DEST, str(current_user.id), album.slug, photo.file)
			img = PilImage.open(photo_path, mode='r')
			
			ratio = (Config.ALBUM_COVER / float(img.size[0]))
			ratio_h = (Config.ALBUM_COVER / float(img.size[1]))
			
			height = int((float(img.size[1]) * float(ratio)))
			width = int((float(img.size[0]) * float(ratio_h)))
			
			if img.size[0] >= img.size[1]:
				img = img.resize((Config.ALBUM_COVER, height), PIL.Image.ANTIALIAS)
			else:
				img = img.resize((width, Config.ALBUM_COVER), PIL.Image.ANTIALIAS)
				
			width, height = img.size
			
			left = (width - Config.ALBUM_COVER) // 2
			top = (height - Config.ALBUM_COVER) // 2
			right = (width + Config.ALBUM_COVER) // 2
			bottom = (height + Config.ALBUM_COVER) // 2
			
			img = img.crop((left, top, right, bottom))
			rgb_im = img.convert('RGB')
			
			img_response = io.BytesIO()
			rgb_im.save(img_response, 'JPEG')
			img_response.seek(0)
		
			return send_file(img_response, attachment_filename='cover.jpg', mimetype='image/jpg', cache_timeout=-1)
			
		except IndexError:
			default = os.path.join(Config.BASE_DIR, 'static', 'images', 'cover.jpg')
			return send_file(default, attachment_filename='cover.jpg', mimetype='image/jpg', cache_timeout=-1)
