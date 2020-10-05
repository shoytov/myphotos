from datetime import datetime
from slugify import slugify
from flask_security import Security, UserMixin, RoleMixin, MongoEngineUserDatastore
from passlib.hash import bcrypt

from init import app, db


class Role(db.Document, RoleMixin):
    """
    класс для фласк секьюрити
    """
    name = db.StringField(max_length=150, verbose_name='Название роли', unique=True)
    description = db.StringField(verbose_name='Описание')

    def __unicode__(self):
        return self.name


class User(db.Document, UserMixin):
    """
    модель пользователя
    """
    email = db.StringField(max_length=50, verbose_name='E-mail', unique=True)
    password = db.StringField(verbose_name='Пароль')
    active = db.BooleanField(default=True)
    roles = db.ListField(db.ReferenceField(Role), default=[])

    @classmethod
    def authenticate(cls, email, password):
        user = cls.objects(email=email).first()
        
        if not bcrypt.verify(password, user.password):
            raise Exception('Invalid password')
        return user

    def save(self):
        if not self.id:
            self.password = bcrypt.hash(self.password)
            return super(User, self).save(self)
        else:
            return super(User, self).update(email=self.email, active=self.active, roles=self.roles)
        
        
class Photo(db.EmbeddedDocument):
    """
    фотография
    """
    file = db.StringField(verbose_name='Название файла')
    created = db.DateTimeField(verbose_name='Дата и время создания')
    device = db.StringField(verbose_name='Устройство')
        
        
class Album(db.Document):
    """
    альбомы с фотографиями пользователя
    """
    user = db.ReferenceField(User, verbose_name='Пользователь')
    name = db.StringField(verbose_name='Название альбома')
    slug = db.StringField(verbose_name='Slug альбома')
    created = db.DateTimeField(default=datetime.now, verbose_name='Дата и время создания')
    description = db.StringField(verbose_name='Описание альбома')
    photos = db.SortedListField(db.EmbeddedDocumentField(Photo), verbose_name='Фотографии')
    
    def save(self):
        self.slug = slugify(self.name, to_lower=True)
        return super(Album, self).save(self)
    
    meta = {
        'indexes': [
            {'fields': ('user', 'name', 'slug'), 'unique': True}
        ]
    }


user_datastore = MongoEngineUserDatastore(db, User, Role)
security = Security(app, user_datastore)
