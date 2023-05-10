import os
from .base_settings import *
import dj_database_url

SECRET_KEY = os.environ['SECRET_KEY']

DEBUG = False

ALLOWED_HOSTS = ['song-bank-prod.herokuapp.com']

DATABASES = {
    'default': dj_database_url.config()
}
