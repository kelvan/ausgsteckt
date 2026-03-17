from ._base import *

DEBUG = False

DEFAULT_FROM_EMAIL = "info@ausgsteckt.ist-total.org"
EMAIL_NOTIFICATION = ["ausgsteckt-admin@ist-total.org"]

STATIC_ROOT = BASE_DIR.parent / "public" / "static"
MEDIA_ROOT = BASE_DIR.parent / "public" / "media"

ALLOWED_HOSTS = ["ausgsteckt.ist-total.org"]
CSRF_TRUSTED_ORIGINS = ["https://ausgsteckt.ist-total.org"]
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

LOG_DIR = BASE_DIR.parent / "log"
LOG_DIR.mkdir(exist_ok=True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            "datefmt": "%d/%b/%Y %H:%M:%S",
        },
    },
    "handlers": {
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": f"{LOG_DIR}/ausgsteckt.log",
            "formatter": "verbose",
        },
        "import_osm_file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": f"{LOG_DIR}/import_osm.log",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "": {
            "handlers": ["file"],
            "level": "INFO",
            "propagate": True,
        },
        "buschenschank.management.commands.import_osm": {
            "handlers": ["import_osm_file"],
            "propagate": False,
        },
        "django.request": {
            "handlers": ["file"],
            "level": "ERROR",
            "propagate": False,
        },
    },
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.memcached.PyMemcacheCache",
        "LOCATION": "127.0.0.1:11211",
    }
}
