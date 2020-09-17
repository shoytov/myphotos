import os


class Config(object):
    HOST = 'http://127.0.0.1:5000'
    BASE_DIR = os.getcwd()
    
    SECRET_KEY = 'sdfsdlkJhghgFD#2342hjhfgd353fgfddg'

    DEBUG = True

    CSRF_ENABLED = True

    MONGODB_SETTINGS = {
        'db': os.environ['DB_NAME'],
        'host': os.environ['DB_HOST'],
        'port': int(os.environ['DB_PORT'])
    }

    WIDTH = 300  # размер миниатюры картинки
    MAX_WIDTH = 1000  # размер картинки при большом выводе
    ALBUM_COVER = 500  # сторона квадрата обложки альбома

    SECURITY_PASSWORD_SALT = 'afadfd-sdfsd3432sdfsf-msfgfd2fEFdfds'
    SECURITY_PASSWORD_HASH = 'sha512_crypt'

    PHOTOS_DIR = 'photos'
    MIN_PHOTOS_DIR = 'min_photos'

    UPLOADS_DEFAULT_DEST = os.path.join(BASE_DIR, PHOTOS_DIR)
    DEFAULT_MIN_DIR = os.path.join(BASE_DIR, MIN_PHOTOS_DIR)
    UPLOADS_DEFAULT_URL = HOST + '/static/img/'

    UPLOADED_IMAGES_DEST = os.path.join(BASE_DIR, 'photos')
    UPLOADED_IMAGES_URL = HOST + '/static/img/'