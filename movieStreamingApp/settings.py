import os
from pathlib import Path
from os import path, getenv
from logging.handlers import RotatingFileHandler
from firebase_admin import storage, initialize_app, credentials

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Firebase setup
BASE_DIR = Path(__file__).resolve().parent.parent
serviceAccount = os.path.join(BASE_DIR, 'firebase', './video-stream-app-6b509-firebase-adminsdk-f62d7-0d43816024.json')
cred = credentials.Certificate(serviceAccount)
buck = 'video-stream-app-6b509.appspot.com'

initialize_app(cred, 
    {'storageBucket': buck}
)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-zo0#&7fk2x^g#elm5kzn3goa-r$4&76vu(j^t$_^g-s&#-c^7l'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ALLOWED_HOSTS = []
ALLOWED_HOSTS = ['arrow112.pythonanywhere.com', 'localhost']

APPEND_SLASH = False

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'movieStreamingApp',
    'movie_app',
    'series_app',
    'auth_app',
    'bookmark_app',
    'search_app',
    'comment_app',
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

ROOT_URLCONF = 'movieStreamingApp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            path.join(BASE_DIR,'rootTemplates'),
            path.join('movieStreamingApp','templates'),
            path.join('movie_app','templates'),
            path.join('auth_app','templates'),
            path.join('bookmark_app','templates'),
            path.join('comment_app','templates'),
            path.join('search_app','templates'),
            path.join('series_app','templates'),
        ],
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

WSGI_APPLICATION = 'movieStreamingApp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'streamingApp',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'localhost',  
        'PORT': '3306',       
    }
}
'''

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR/'rootStatic',
    BASE_DIR/'movie_app'/'static',
    BASE_DIR/'auth_app'/'static',
    BASE_DIR/'series_app'/'static',
    BASE_DIR/'comment_app'/'static',
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SESSION_COOKIE_AGE = 172800
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_SAVE_EVERY_REQUEST = False

LOGIN_URL = '/auth/login/'

LOGGING = {
    "version": 1,  # the dictConfig format version
    "disable_existing_loggers": False,  # retain the default loggers
    "handlers": {
        "file": {
            #"class": "logging.FileHandler",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "general.log",
            "level": "DEBUG",
            "formatter": "verbose",
            'backupCount': 10, # keep at most 10 log files
            'maxBytes': 5242880, # 5*1024*1024 bytes (5MB)
        },
    },
    "loggers": {
        "": {
            "level": "DEBUG",
            "handlers": ["file"],
        },
    },
    "formatters": {
        "verbose": {
            "format": "{name} {levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
}