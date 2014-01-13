"""
Django settings for dormbase project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# the name of the app that this settings file lives in
SITE_APP_NAME = "sampledorm"

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SITE_DIR = os.path.join(BASE_DIR, SITE_APP_NAME)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'x#$^gh0^io3_)x564h99byqx+zfi3w7gfwsq6dlwmy0#b9qp-('

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django_extensions',
    'photologue',
    'autocomplete_light',
    'guardian',
    'south',
    SITE_APP_NAME,
    # pick which Dormbase apps you want:
    'common',
    'desk',
    'deskitem',
    'facilities',
    'guestlist',
    'laundry',
    'menus',
    'mitauth',
    'nextbus',
    'package',
    'personal',
    'residents',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'mitauth.auth.CertificateRemoteUserMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'mitauth.auth.CertificateRemoteUserBackend',
    'mitauth.auth.CertificateFreeTestingBackend',
    'django.contrib.auth.backends.ModelBackend',
    'guardian.backends.ObjectPermissionBackend',
)

# for django-guardian
ANONYMOUS_USER_ID = -1

ROOT_URLCONF = '%s.urls' % SITE_APP_NAME

WSGI_APPLICATION = '%s.wsgi.application' % SITE_APP_NAME

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

STATIC_URL = '/static/'

TEMPLATE_DIRS = (
    os.path.join(SITE_DIR, "templates"),
)

# for the sites framework

SITE_ID = 1
DOMAIN_NAME = "localhost"
DORM_NAME = "Sample Dorm"
BUILDING = "W79"

# options that each dorm ("site") can customize

IS_UNDERGRAD_DORM = True
DESKWORKER_GROUP_NAME = "Deskworkers"
HOUSETEAM_GROUP_NAME = "House Team"
GROUPS_TO_CREATE = [DESKWORKER_GROUP_NAME, HOUSETEAM_GROUP_NAME]

# execute private settings file

if os.path.exists("settings_private.py"):
    execfile("settings_private.py")
