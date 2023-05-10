from .base_settings import *

DEBUG = True

SECRET_KEY = 'django-insecure-*bl5-ith0jy=qa*twh4o+dq^384fjw1oyi$%psgftqlxt*=0!#'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'songBank',
        'HOST': 'localhost',
        'USER': 'root',
        'PASSWORD': '@#$Ecf1173092331',
        'PORT': '3306',
    }
}