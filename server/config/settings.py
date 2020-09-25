import os

import sentry_sdk
import dj_database_url
from sentry_dramatiq import DramatiqIntegration
from sentry_sdk.integrations.django import DjangoIntegration

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'

ALLOWED_HOSTS = ['*']
CORS_ALLOW_ALL_ORIGINS = True
SITE_ID = 1

DEBUG = os.getenv('DEBUG', 'True') == 'True'
SECRET_KEY = os.getenv('SECRET_KEY', 'khgfgshGKL834asjgs2345afgljaskdjAGJHD647ASDASDF')
ENVIRONMENT = os.getenv('ENVIRONMENT', 'local')

##################################################################
# Custom user settings
##################################################################

AUTH_USER_MODEL = 'api.UserAccount'

##################################################################
# Auto slug settings
##################################################################

AUTOSLUG_SLUGIFY_FUNCTION = 'pytils.translit.slugify'

##################################################################
# Databases settings
##################################################################

DATABASES = {'default': dj_database_url.config()}

##################################################################
# Locale settings
##################################################################

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True
USE_L10N = True
USE_TZ = True

##################################################################
# Logging settings
##################################################################

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'request_properties': {
            '()': 'api.services.CustomRequestPropertiesFilter'
        },
    },
    'formatters': {
        'standard': {
            '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
            'format': '%(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'filters': [
                'request_properties',
            ],
            'formatter': 'standard',
        },
    },
    'loggers': {
        'api': {
            'handlers': ('console',),
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ('console',),
            'level': 'INFO',
            'propagate': False,
        },
    }
}

##################################################################
# Installed applications
##################################################################

INSTALLED_APPS = [
    'admin_tools',
    'admin_tools.theming',
    'admin_tools.menu',
    'admin_tools.dashboard',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'corsheaders',
    'rest_framework',

    'django_json_widget',

    'django_dramatiq',
    'django_periodiq',
]

LOCAL_APPS = [
    'api'
]

INSTALLED_APPS += LOCAL_APPS

MIGRATION_MODULES = {app_name: f'migrations.{app_name}' for app_name in LOCAL_APPS}

##################################################################
# Caches settings
##################################################################

CACHES = {
    'default': {
        'BACKEND': 'redis_lock.django_cache.RedisCache',
        'LOCATION': os.getenv('CACHE_REDIS_URL', 'redis://127.0.0.1:6380/1'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

##################################################################
# Dramatiq settings
##################################################################

DRAMATIQ_BROKER = {
    'BROKER': 'dramatiq.brokers.redis.RedisBroker',
    'OPTIONS': {
        'url': os.getenv('DRAMATIQ_BROKER_REDIS_URL', 'redis://127.0.0.1:6380/2')
    },
    'MIDDLEWARE': [
        'periodiq.PeriodiqMiddleware',
        'dramatiq.middleware.AgeLimit',
        'dramatiq.middleware.TimeLimit',
        'dramatiq.middleware.Callbacks',
        'dramatiq.middleware.Retries',
        'dramatiq.middleware.Pipelines',
        'django_dramatiq.middleware.DbConnectionsMiddleware',
    ]
}

DRAMATIQ_RESULT_BACKEND = {
    'BACKEND': 'dramatiq.results.backends.redis.RedisBackend',
    'BACKEND_OPTIONS': {
        'url': os.getenv('DRAMATIQ_RESULT_BACKEND_REDIS_URL', 'redis://127.0.0.1:6380/3')
    },
    'MIDDLEWARE_OPTIONS': {
        'result_ttl': 60000
    }
}

##################################################################
# Templates, middleware settings
##################################################################

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': False,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.static',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
                'admin_tools.template_loaders.Loader',
            ]
        },
    },
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'api.middlewares.CustomRequestPropertiesMiddleware',
]

##################################################################
# Password validation settings
##################################################################

if not DEBUG:
    AUTH_PASSWORD_VALIDATORS = [
        {
            'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
            'OPTIONS': {
                'min_length': 6,
            }
        },
        {
            'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
        },
    ]

##################################################################
# Static files settings (CSS, JavaScript, Images)
##################################################################

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = ('static',)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

FILE_UPLOAD_PERMISSIONS = 0o777
FILE_UPLOAD_DIRECTORY_PERMISSIONS = 0o777

##################################################################
# Notification error to sentry settings
##################################################################

SENTRY_DSN = os.getenv('SENTRY_DSN', '')

if SENTRY_DSN:
    sentry_sdk.init(
        SENTRY_DSN,
        integrations=[DjangoIntegration(), DramatiqIntegration()],
        attach_stacktrace=True,
        send_default_pii=True,
        in_app_exclude=[
            'django',
            'sentry',
            'rest_framework',
        ]
    )

##################################################################
# DRF settings
##################################################################

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'api.authentication.CustomTokenAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework_json_api.renderers.JSONRenderer',
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework_json_api.parsers.JSONParser',
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ),

    # Used query parameters page[number] and page[size]
    'DEFAULT_PAGINATION_CLASS': 'rest_framework_json_api.pagination.JsonApiPageNumberPagination',
    'PAGE_SIZE': 20,

    'DATETIME_FORMAT': '%Y-%m-%dT%H:%M:%S.%f%z',
    'SEARCH_PARAM': 'filter[search]',

    'TEST_REQUEST_DEFAULT_FORMAT': 'vnd.api+json',
    'TEST_REQUEST_RENDERER_CLASSES': (
        'rest_framework_json_api.renderers.JSONRenderer',
    ),
}

JSON_API_UNIFORM_EXCEPTIONS = True
