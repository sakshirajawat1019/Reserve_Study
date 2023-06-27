# ALLOWED_HOSTS = ['a724-103-180-81-98.ngrok-free.app']
# '198.211.99.20', 'localhost', '127.0.0.1:8000', 

ALLOWED_HOSTS = ['*']

DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'reserve_study',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '5432',
        'OPTIONS': {
            'sslmode': 'require'
        }
    }
}

from .base import *

CORS_ORIGIN_WHITELIST = [
    'https://localhost:3000',
    'http://localhost:3000',
]