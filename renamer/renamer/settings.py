"""
Django settings for renamer project.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# check https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ["APP_SECRET_KEY"]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [os.environ["VIRTUAL_HOST"], "localhost"]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_celery_results',
    'imageadmin'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'renamer.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'renamer.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
#
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': os.environ['DB_POSTGRES_PW'],
        'HOST': 'db',
        'PORT': 5432,
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LOGIN_URL = 'login/'

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'imageadmin/static/'
STATIC_ROOT = '/webapp/renamer/static'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Setup support for proxy headers
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

#
# imageadmin application settings
#
ARCHIVE_LOCATION = os.environ['ARCHIVE_LOCATION']
INCOMING_LOCATION = os.environ['INCOMING_LOCATION']
DIVA_LOCATION = os.environ['DIVA_LOCATION']
DATA_LOCATION = os.environ['DATA_LOCATION']
BACKUP_LOCATION = os.environ['BACKUP_LOCATION']
TMPDIR = os.environ['APP_TMPDIR']


PATH_TO_GS = "/usr/bin/gs"
PATH_TO_GM = "/usr/bin/gm"
#PATH_TO_VIPS = "/usr/bin/vips"
PATH_TO_SHASUM = "/usr/bin/shasum"
PATH_TO_KDU = "/usr/local/bin/kdu_compress"

# IIIF-Presentation manifests
IIIF_MANIF_BASE_URL = os.environ['IIIF_MANIF_BASE_URL']
IIIF_IMAGE_BASE_URL = os.environ['IIIF_IMAGE_BASE_URL']
# IIIF-Auth (optional)
IIIF_LOGIN_URL = os.environ.get('IIIF_LOGIN_URL')
IIIF_LOGOUT_URL = os.environ.get('IIIF_LOGOUT_URL')
IIIF_TOKEN_URL = os.environ.get('IIIF_TOKEN_URL')

CELERY_IMPORTS = ("imageadmin.helpers.to_archive",
                  "imageadmin.helpers.to_diva",
                  "imageadmin.helpers.generate_json")

CELERY_BROKER_URL = 'amqp://guest@broker:5672//'

CELERY_RESULT_BACKEND = 'django-db'
#CELERY_RESULT_BACKEND = "database"
#CELERY_DATABASE_URL = "sqlite:///db.sqlite"

