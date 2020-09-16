from flask import Blueprint, render_template, request, redirect
from flask_login import logout_user

from gallery.services.check_user_login import CheckUserLogin
from gallery.services.user_login import UserLogin
from gallery.services.get_user_albums import GetUserAlbums
from gallery.services.add_user_album import AddUserAlbum
from gallery.services.view_album import ViewAlbum
from gallery.services.upload_photos import UploadPhotos
from gallery.services.get_photo_file import GetPhotoFile
from gallery.services.delete_album import DeleteAlbum
from gallery.services.photo_stream import PhotoStream
from gallery.services.show_photo import ShowPhoto
from gallery.services.delete_photo import DeletePhoto
from gallery.services.filter_by_camera import FilterByCamera
from .forms import LoginForm, AddAlbumForm, AddPhotosForm

gallery = Blueprint('gallery', __name__, template_folder='templates')


@gallery.route('/')
def index():
	"""
	главная страница
	"""
	if not CheckUserLogin.check():
		form = LoginForm()
		return render_template('login.html', form=form)
	else:
		photos = PhotoStream.stream()

		return render_template('gallery.html', photos=photos)
	
	
@gallery.route('/login/', methods=['POST'])
def login():
	"""
	логин пользователя
	"""
	login = UserLogin(request.form.get('username'), request.form.get('password'))
	
	if login.login():
		return redirect('/')
	else:
		form = LoginForm(request.form)
		return render_template('login.html', form=form, message='Неверные данные')
	
	
@gallery.route('/logout/')
def logout():
	"""
	разлогинивание пользователя
	"""
	logout_user()
	return redirect('/')


@gallery.route('/albums/')
def albums():
	"""
	вывод альбомов пользователя
	"""
	if not CheckUserLogin.check():
		return redirect('/')
	
	albums = GetUserAlbums.get()
	return render_template('albums.html', albums=albums)


@gallery.route('/add-album/', methods=['GET', 'POST'])
def add_album():
	"""
	добавление нового альбома пользователем
	"""
	if request.method == 'GET':
		form = AddAlbumForm()
		return render_template('add_album.html', form=form)
	else:
		album = AddUserAlbum(request.form.get('name'), request.form.get('description'))
		album.add()
		return redirect('/albums/')
	
	
@gallery.route('/album/<slug>/')
def album(slug: str):
	"""
	вывод альбома
	"""
	album = ViewAlbum(slug)
	form = AddPhotosForm()
	form.slug.data = slug
	return render_template('album.html', album=album.album(), devices=album.get_devices(), form=form)


@gallery.route('/upload-photos/', methods=['POST'])
def upload_photos():
	"""
	загрузка фотографий пользователем в альбом
	"""
	UploadPhotos.upload()
	return redirect('/album/{}/'.format(request.form.get('slug')))


@gallery.route('/get-photo/<album_id>/<filename>/<file_type>/')
def get_photo(album_id: str, filename: str, file_type: str='min'):
	"""
	вывод файла фотографии
	"""
	if not CheckUserLogin.check():
		return
	
	file = GetPhotoFile(album_id, filename, file_type)
	return file.get()


@gallery.route('/delete-album/<album_id>/')
def delete_album(album_id: str):
	"""
	удаление альбома пользователя со всеми фотографиями
	"""
	if not CheckUserLogin.check():
		return
	
	deleted = DeleteAlbum(album_id)
	deleted.delete()
	return redirect('/albums/')


@gallery.route('/show-photo/<album_id>/<file>/')
def show_photo(album_id: str, file: str):
	"""
	вывод оригинала фотографии
	"""
	if not CheckUserLogin.check():
		return redirect('/')
	
	res = ShowPhoto(album_id, file)
	photo, photo_prev, photo_next = res.show()
	
	return render_template('show_photo.html', photo=photo, photo_prev=photo_prev, photo_next=photo_next)


@gallery.route('/delete-photo/<album_id>/<file>/')
def delete_photo(album_id: str, file: str):
	"""
	удаление фотографии
	"""
	if not CheckUserLogin.check():
		return redirect('/')
	
	deleted = DeletePhoto(album_id, file)
	album_slug = deleted.delete()
	return redirect('/album/{}'.format(album_slug))


@gallery.route('/filter/<album_slug>/<camera>/')
def filter(album_slug: str, camera: str):
	if not CheckUserLogin.check():
		return redirect('/')
	
	photos = FilterByCamera(album_slug, camera)
	return render_template('filtered_photos.html', photos=photos.filter(), filter=camera)
