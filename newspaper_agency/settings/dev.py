from newspaper_agency.settings.base import *


SECRET_KEY = 'django-insecure-#-0-+_v2&_o1k5qur5i@(ra+f8e@rdwl70z$)^s*4*ca1rm(v6'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}