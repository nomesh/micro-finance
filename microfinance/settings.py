from __future__ import absolute_import
import os
import djcelery
from datetime import timedelta
from celery.schedules import crontab
import dj_database_url

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'y409=qwy(=u^%7t$aa)j=83^f!-oqyy2omq%pj1+koeh2aryvd')

DEBUG = os.environ.get('DEBUG', 'True') == 'True'


ALLOWED_HOSTS = ['localhost', '127.0.0.1', '.onrender.com', '.railway.app']
if os.environ.get('RENDER_EXTERNAL_HOSTNAME'):
    ALLOWED_HOSTS.append(os.environ.get('RENDER_EXTERNAL_HOSTNAME'))
if os.environ.get('RAILWAY_PUBLIC_DOMAIN'):
    ALLOWED_HOSTS.append(os.environ.get('RAILWAY_PUBLIC_DOMAIN'))

# Site URL for email links
SITE_URL = os.environ.get('SITE_URL', 'http://localhost:8000')
if os.environ.get('RAILWAY_PUBLIC_DOMAIN'):
    SITE_URL = f"https://{os.environ.get('RAILWAY_PUBLIC_DOMAIN')}"
elif os.environ.get('RENDER_EXTERNAL_HOSTNAME'):
    SITE_URL = f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}"

PHOTO_PATH = 'static/images/users'
SIGNATURE_PATH = 'static/images/signatures'

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'micro_admin',
    'savings',
    'loans',
    'core',
    'compressor',
    'celery',
    'djcelery',
    'kombu.transport.django',
    'simple_pagination',
    'django_blog_it.django_blog_it',
)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'microfinance.urls'

WSGI_APPLICATION = 'microfinance.wsgi.application'

AUTH_USER_MODEL = 'micro_admin.User'

LOGIN_URL = '/'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

STATICFILES_DIRS = (BASE_DIR + '/static',)

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_ROOT = BASE_DIR

# Database configuration
if 'DATABASE_URL' in os.environ:
    DATABASES = {'default': dj_database_url.config(conn_max_age=600)}
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

# WhiteNoise for static files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

# Compress Settings
COMPRESS_ROOT = BASE_DIR + '/static/'

COMPRESS_ENABLED = True

COMPRESS_OFFLINE_CONTEXT = {
    'STATIC_URL': 'STATIC_URL',
}

COMPRESS_CSS_FILTERS = ['compressor.filters.css_default.CssAbsoluteFilter', 'compressor.filters.cssmin.CSSMinFilter']
COMPRESS_JS_FILTERS = ['compressor.filters.jsmin.JSMinFilter']
COMPRESS_REBUILD_TIMEOUT = 5400


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR + "/templates/"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors':
            [
                "django.contrib.auth.context_processors.auth",
                'django.template.context_processors.request',
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

djcelery.setup_loader()
BROKER_URL = 'django://'
CELERY_IMPORTS = ("micro_admin.tasks")
# BROKER_URL = 'redis://localhost:6379/0'
CELERY_TIMEZONE = 'UTC'
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
CELERYBEAT_SCHEDULE = {
    'add-interest-every-day-midnight': {
        'task': 'micro_admin.tasks.calculate_interest_of_savings_account',
        # 'schedule': timedelta(seconds=15),
        'schedule': crontab(minute='0', hour='0'),
        # 'schedule': crontab(minute=0, hour=0) Execute daily at midnight.
    }
    # 'add-every-1-minute': {
    #     'task': 'micro_admin.tasks.add',
    #     'schedule': crontab(minute='*/1'),
    #     'args': (16, 16)
    # },
    # 'add-every-30-seconds': {
    #     'task': 'micro_admin.tasks.add',
    #     'schedule': timedelta(seconds=30),
    #     'args': (25, 25)
    # },
}
