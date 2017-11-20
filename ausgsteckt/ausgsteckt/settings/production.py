from ._base import *

DEBUG = False

DEFAULT_FROM_EMAIL = 'info@ausgsteckt.ist-total.org'
EMAIL_NOTIFICATION = ['ausgsteckt-admin@ist-total.org']

STATIC_ROOT = os.path.join(BASE_DIR, '..', 'public', 'static/')
MEDIA_ROOT = os.path.join(BASE_DIR, '..', 'public', 'media/')

ALLOWED_HOSTS = [
    'ausgsteckt.ist-total.org'
]

# pipeline keeps fucking up map js files
PIPELINE['PIPELINE_ENABLED'] = False

LOG_DIR = os.path.join(os.path.dirname(BASE_DIR), 'log')
if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s',
            'datefmt': '%d/%b/%Y %H:%M:%S'
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '%s/ausgsteckt.log' % LOG_DIR,
            'formatter': 'verbose'
        },
        'import_osm_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '%s/import_osm.log' % LOG_DIR,
            'formatter': 'verbose'
        },
    },
    'loggers': {
        '': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
        'buschenschank.management.commands.import_osm': {
            'handlers': ['import_osm_file'],
            'propagate': False,
        },
        'django.request': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': False,
        },
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

try:
    from .sentry_settings import DSN
    import raven

    INSTALLED_APPS.append(
        'raven.contrib.django.raven_compat'
    )
    RAVEN_CONFIG = {
        'dsn': DSN,
        'release': raven.fetch_git_sha(os.path.dirname(BASE_DIR)),
    }
except ImportError:
    pass
