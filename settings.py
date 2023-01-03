import os
from pathlib import Path

import dj_database_url
from dotenv import load_dotenv

load_dotenv('.env.local')

BASE_DIR = Path(__file__).resolve().parent
DB_CONNECTION_URL = os.environ.get('DB_CONNECTION_URL')
RUN_ON_REAL_SERVER = os.environ.get('RUN_ON_REAL_SERVER', 'false')

DEBUG = RUN_ON_REAL_SERVER != 'true'

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-_fj0b612=*&$*&*u9)w70r3$5k9nf8um!&hyfbv7dfx@_#ri)g')

ROOT_URLCONF = 'discuss_api.urls'

WSGI_APPLICATION = 'discuss_api.wsgi.application'

ALLOWED_HOSTS = ['*']

CORS_ALLOW_ALL_ORIGINS = True

INSTALLED_APPS = [
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'discuss_api.apps.status',
    'discuss_api.apps.agenda',
    'discuss_api.apps.tag',
    'discuss_api.apps.member',
    'discuss_api.apps.multi_auth',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

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

DATABASES = {
    'default': dj_database_url.parse(DB_CONNECTION_URL),
}

AUTH_PASSWORD_VALIDATORS = [{
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    }, {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    }, {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    }, {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LANGUAGE_CODE = 'ko-kr'
TIME_ZONE = 'Asia/Seoul'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
# DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
# GS_BUCKET_NAME = os.environ.get('BUCKET_NAME')
# GS_QUERYSTRING_AUTH = False
# GS_FILE_OVERWRITE = False

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

TWITTER_CONSUMER_KEY = os.environ.get('TWITTER_CONSUMER_KEY')
TWITTER_CONSUMER_SECRET = os.environ.get('TWITTER_CONSUMER_SECRET')
FB_CLIENT_ID = os.environ.get('FB_CLIENT_ID')
FB_CLIENT_SECRET = os.environ.get('FB_CLIENT_SECRET')
GITHUB_CLIENT_ID = os.environ.get('GITHUB_CLIENT_ID')
GITHUB_CLIENT_SECRET = os.environ.get('GITHUB_CLIENT_SECRET')
