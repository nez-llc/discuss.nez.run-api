import os
from pathlib import Path

import dj_database_url
from dotenv import load_dotenv


load_dotenv('.env.local')


BASE_DIR = Path(__file__).resolve().parent

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-_fj0b612=*&$*&*u9)w70r3$5k9nf8um!&hyfbv7dfx@_#ri)g'

ROOT_URLCONF = 'discuss_api.urls'

WSGI_APPLICATION = 'discuss_api.wsgi.application'

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'discuss_api.apps.status',
    # 'discuss_api.apps.question',
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
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
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

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
