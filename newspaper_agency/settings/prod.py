from newspaper_agency.settings.base import *
import os


SECRET_KEY = os.environ['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1", "newspaper-agency-cwzg.onrender.com"]


RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
   ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases



DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.postgresql',
       'NAME': os.environ['POSTGRES_DB'],
       'USER': os.environ['POSTGRES_USER'],
       'PASSWORD': os.environ['POSTGRES_PASSWORD'],
       'HOST': os.environ['POSTGRES_HOST'],
       'PORT': os.environ['POSTGRES_DB_PORT'],
       'OPTIONS': {
           'sslmode': 'require',
       },
   }
}
