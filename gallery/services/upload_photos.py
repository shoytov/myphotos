import os
from datetime import datetime
from operator import itemgetter
from flask import request
from flask_security import current_user
from PIL import Image as PilImage
import PIL
from PIL.ExifTags import TAGS

from config import Config
from init import photos
from models import Album, Photo

class UploadPhotos(object):
	"""
	загрузка фотографий пользователем в альбом
	"""
	@staticmethod
	def upload():
		path = os.path.join(Config.UPLOADS_DEFAULT_DEST, str(current_user.id), request.form.get('slug'))
		path_min = os.path.join(Config.DEFAULT_MIN_DIR, str(current_user.id), request.form.get('slug'))
		
		# создаем директорию для фоток, если ее нет
		if not os.path.isdir(path):
			os.makedirs(path)
			
		# создаем директорию для миниатюр, если ее нет
		if not os.path.isdir(path_min):
			os.makedirs(path_min)
		
		album = Album.objects(slug=request.form.get('slug', ''), user=current_user.id).get()
		
		photos_list = album.photos
		for img in request.files.getlist("images"):
			if img.filename:
				file_path = photos.save(img, folder=path)
				filename = file_path.split('/')[-1]
				
				image = PilImage.open(file_path)
				exif_data = image.getexif()
				device = None
				created = None
				
				for tag_id in exif_data:
					tag = TAGS.get(tag_id, tag_id)
					data = exif_data.get(tag_id)
					try:
						if isinstance(data, bytes):
							data = data.decode()
						
						if f"{tag:25}".find('Model') == 0:
							device = data
						if f"{tag:25}".find('DateTimeOriginal') == 0:
							created = data
					except:
						pass
				
				ratio = (Config.WIDTH / float(image.size[0]))
				height = int((float(image.size[1]) * float(ratio)))
				image = image.resize((Config.WIDTH, height), PIL.Image.ANTIALIAS)
				file_min_path = image.save(os.path.join(path_min, filename))
				
				photo = Photo()
				photo.file = filename
				photo.device = device
				if created:
					photo.created = datetime.strptime(created, '%Y:%m:%d %H:%M:%S')
				
				photos_list.append(photo)
		
		# сортируем фотографии по дате создания в обратном порядке
		try:
			photos_list = sorted(photos_list, key=itemgetter('created'), reverse=True)
		except TypeError:
			photos_list = sorted(photos_list, key=itemgetter('file'))
		
		album.update(photos=photos_list)
