from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, MultipleFileField, HiddenField
from flask_wtf.file import FileAllowed
from wtforms.validators import InputRequired

from init import photos


class LoginForm(FlaskForm):
    """
    форма авторизации
    """
    username = StringField('Логин', description='логин', validators=[InputRequired()])
    password = PasswordField('Пароль', description='пароль', validators=[InputRequired()])
    
    
class AddAlbumForm(FlaskForm):
    """
    форма добавления нового альбома пользователем
    """
    name = StringField('Название альбома', description='Название альбома', validators=[InputRequired()])
    description = TextAreaField('Описание альбома', description='Описание альбома')
    
    
class AddPhotosForm(FlaskForm):
    """
    форма добавления фотографий в альбом
    """
    slug = HiddenField()
    images = MultipleFileField('Выберите файлы для загрузки', validators=[FileAllowed(photos, 'Image only!')])
