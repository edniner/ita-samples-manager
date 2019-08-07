"""
Django settings for test-irrad-management-page project.

Generated by 'django-admin startproject' using Django 1.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

STATIC_ROOT = os.path.join(BASE_DIR, 'static', )
STATIC_URL = 'http://test-irrad-management-page.web.cern.ch/static/'


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ma_nu+jq0tcka72kv2rls1+dv6^&0@i7v3#mi(nmzcp7h1f+q-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

DEFAULT_FROM_EMAIL = 'irrad.ps@cern.ch'
SERVER_EMAIL = 'irrad.ps@cern.ch'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.cern.ch'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'Irradiation.Facilities@cern.ch'
EMAIL_HOST_PASSWORD = 'Maurice010'

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'widget_tweaks',
    'pytz',
    'django.contrib.admindocs',
    #Don't forget to uncomment this part in production!!!
    'mod_wsgi.server',
    'samples_manager',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'samples_manager.remuser.ProxyRemoteUserMiddleware',
    #'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    #'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Uncomment this in production!!!!
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.RemoteUserBackend',
    'django.contrib.auth.backends.ModelBackend',
]

ROOT_URLCONF = 'test-irrad-management-page.urls'

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

WSGI_APPLICATION = 'wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

#This setting on production
"""DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.oracle',
        'NAME': 'pdbr-s.cern.ch:10121/pdbr.cern.ch',
        'USER': 'ps_irrad_admin',
        'PASSWORD': 'RadmonAdmin010',
        'OPTIONS': {'threaded': True}
    }
}
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.oracle',
        'NAME': 'devdb11-s.cern.ch:10121/devdb11.cern.ch',
        'USER': 'ps_irrad_admin',
        'PASSWORD': 'RadmonAdmin010',
        'OPTIONS': {'threaded': True}
    }
}

"""DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
"""

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Zurich'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DATE_INPUT_FORMATS='%d/%m/%Y'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

#Uncomment this in production!!!!
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

INTERNAL_IPS = ['127.0.0.1']
