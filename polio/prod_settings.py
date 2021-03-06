import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '7i_%j5chyhx2k3#874-!8kwwlcr88sn9blbsb7$%58h&t#n84f' # make this envi var

DEBUG = True
TEMPLATE_DEBUG = False

ALLOWED_HOSTS = []

LOGIN_REDIRECT_URL = '/datapoints'
MEDIA_ROOT = '/var/www/clients.seedscientific.com/uf/UF04/polio/media/'
MEDIA_URL = '/var/www/clients.seedscientific.com/uf/UF04/polio/media/'

INSTALLED_APPS = (
    'south',
    'django_admin_bootstrapped.bootstrap3',
    'django_admin_bootstrapped',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'source_data',
    'datapoints',
    'simple_history',
    'coverage',
    # 'stronghold',
    'csvimport',
    'guardian',
    'tastypie',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'stronghold.middleware.LoginRequiredMiddleware'
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend', # this is default
    'guardian.backends.ObjectPermissionBackend',
)


ANONYMOUS_USER_ID = -1

ROOT_URLCONF = 'polio.urls'
WSGI_APPLICATION = 'polio.wsgi.application'

## DATABASE ##

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'polio',
        'USER': 'djangoapp',
        'PASSWORD': 'w3b@p01i0',
        'HOST': '50.57.77.252',
        'PORT': '5432',
    }
}

## INTERNATIONALIZATION ##
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'EST'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# STATIC FILES (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'


## API SETTINGS ###
TASTYPIE_DEFAULT_FORMATS = ['json']
API_LIMIT_PER_PAGE = 0
TASTYPIE_FULL_DEBUG = True
