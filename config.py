class Config(object):
    SECRET_KEY = 'sdfsdlkJhghgFD#2342hjhfgd353fgfddg'

    DEBUG = True

    CSRF_ENABLED = True

    MONGODB_SETTINGS = {
        'db': 'myphotos',
        'host': '127.0.0.1',
        'port': 27017
    }

    SECURITY_PASSWORD_SALT = 'afadfd-sdfsd3432sdfsf-msfgfd2fEFdfds'
    SECURITY_PASSWORD_HASH = 'sha512_crypt'