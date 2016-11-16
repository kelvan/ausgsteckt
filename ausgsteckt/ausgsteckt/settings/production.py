from ._base import *

DEBUG = False

DEFAULT_FROM_EMAIL = 'ausgsteckt@ist-total.org'
EMAIL_NOTIFICATION = ['ausgsteckt-admin@ist-total.org']

STATIC_ROOT = os.path.join(BASE_DIR, '..', 'public', 'static/')
MEDIA_ROOT = os.path.join(BASE_DIR, '..', 'public', 'media/')

ALLOWED_HOSTS = [
    'ausgsteckt.ist-total.org'
]

LOG_DIR = os.path.join(os.path.dirname(BASE_DIR), 'log')
if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '%s/ausgsteckt.log' % LOG_DIR,
            'formatter': 'verbose'
        },
    },
    'loggers': {
        '': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
