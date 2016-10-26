from ._base import *

DEBUG = False

DEFAULT_FROM_EMAIL = 'ausgsteckt@ist-total.org'
EMAIL_NOTIFICATION = ['ausgsteckt-admin@ist-total.org']

STATIC_ROOT = os.path.join(BASE_DIR, '..', 'public', 'static/')
MEDIA_ROOT = os.path.join(BASE_DIR, '..', 'public', 'media/')

ALLOWED_HOSTS = [
    # TODO
]
