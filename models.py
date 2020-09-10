from init import app, db
from flask_security import Security, UserMixin, RoleMixin, MongoEngineUserDatastore
from passlib.hash import bcrypt


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
        user = cls.query.filter(cls.email == email).one()
    
        if not bcrypt.verify(password, user.password):
            raise Exception('Invalid password')
        return user

    def save(self):
        if not self.id:
            self.password = bcrypt.hash(self.password)
            return super(User, self).save(self)
        else:
            return super(User, self).update(email=self.email, active=self.active, roles=self.roles)


user_datastore = MongoEngineUserDatastore(db, User, Role)
security = Security(app, user_datastore)
