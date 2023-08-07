import logging
import os

import environ

from .conf import DjangoConfig

config = DjangoConfig()

logger = logging.getLogger(__name__)

env = environ.Env()

BASE_DIR = config.base_dir
DATA_DIR = config.public_root or (BASE_DIR.parent / "public")

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "el5m47jko&tz)i-qw_@b5wp=6ots)o3qcv^ekrceu$fcm1@jll"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config.debug

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.flatpages",
    "django.contrib.gis",
    "easy_thumbnails",
    "pipeline",
    "ckeditor",
    "ausgsteckt",
    "buschenschank",
    "data_quality",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "ausgsteckt.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "buschenschank.context_processors.region_list",
            ],
        },
    },
]

WSGI_APPLICATION = "ausgsteckt.wsgi.application"

TEST_RUNNER = "xmlrunner.extra.djangotestrunner.XMLTestRunner"
TEST_OUTPUT_DESCRIPTIONS = env.bool("TEST_OUTPUT_DESCRIPTIONS", default=False)
TEST_OUTPUT_DIR = env("TEST_OUTPUT_DIR", default=".")
TEST_OUTPUT_FILE_NAME = env("TEST_OUTPUT_FILE_NAME", default="report.xml")

DATABASES = {
    "default": env.db('DJANGO_DATABASE_URL', default='postgis:///ausgsteckt'),
}
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

SITE_ID = config.site_id

LANGUAGE_CODE = "de-at"


def ugettext(s):
    return s


LANGUAGES = (
    ("de", ugettext("German")),
    ("en", ugettext("English")),
)

LOCALE_PATHS = (os.path.join(BASE_DIR, "locale"),)
TIME_ZONE = config.timezone
USE_I18N = config.use_i18n
USE_L10N = config.use_l10n
USE_TZ = config.use_tz

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", env("HTTP_X_FORWARDED_PROTO", default="http"))

STATIC_URL = config.static_url
MEDIA_URL = config.media_url
MEDIA_ROOT = DATA_DIR / "media"
STATIC_ROOT = DATA_DIR / "static"

CACHE_BACKEND = config.cache_backend

STATICFILES_DIRS = [
    os.path.join(BASE_DIR.parent, "node_modules"),
]

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "pipeline.finders.CachedFileFinder",
)
STATICFILES_STORAGE = "pipeline.storage.PipelineStorage"

PIPELINE = {
    "PIPELINE_ENABLED": True,
    "JS_COMPRESSOR": "pipeline.compressors.NoopCompressor",
    "JAVASCRIPT": {
        "map": {
            "source_filenames": (
                "leaflet/dist/leaflet.js",
                "leaflet-providers/leaflet-providers.js",
                "leaflet-plugins/control/Permalink.js",
                "leaflet-plugins/control/Permalink.Marker.js",
                "leaflet-plugins/control/Permalink.Layer.js",
                "leaflet-plugins/control/Permalink.Overlay.js",
                "js/leaflet.markercluster.js",
                "js/buschenschank/map.js",
            ),
            "output_filename": "js/maps.js",
        },
        "libs": {
            "source_filenames": (
                "jquery/dist/jquery.min.js",
                "popper.js/dist/umd/popper.js",
                "bootstrap/dist/js/bootstrap.min.js",
            ),
            "output_filename": "js/libs.js",
        },
    },
    "CSS_COMPRESSOR": "pipeline.compressors.NoopCompressor",
    "STYLESHEETS": {
        "main": {"source_filenames": ("css/main.css",), "output_filename": "css/main.css"},
        "map": {
            "source_filenames": (
                "css/buschenschank/map.css",
                "leaflet/dist/leaflet.css",
                "css/MarkerCluster.css",
                "css/MarkerCluster.Default.css",
            ),
            "output_filename": "css/maps.css",
        },
        "libs": {
            "source_filenames": (
                "bootstrap/dist/css/bootstrap.min.css",
                "@fortawesome/fontawesome-free/css/fontawesome.min.css",
                "@fortawesome/fontawesome-free/css/solid.min.css",
            ),
            "output_filename": "css/libs.css",
        },
    },
}

THUMBNAIL_ALIASES = {
    "": {
        "details": {"size": (150, 0), "crop": False},
        "dropdown": {"size": (15, 15), "crop": False},
        "list": {"size": (25, 25), "crop": False},
    },
}

CKEDITOR_CONFIGS = {
    "flatpage": {
        "toolbar": "Custom",
        "toolbar_Custom": [
            ["Format", "Bold", "Italic", "Underline"],
            [
                "NumberedList",
                "BulletedList",
                "-",
                "Outdent",
                "Indent",
                "-",
                "JustifyLeft",
                "JustifyCenter",
                "JustifyRight",
                "JustifyBlock",
            ],
            ["Link", "Unlink"],
            ["RemoveFormat", "Source"],
        ],
    }
}

# OSM settings

OVERPASS_ENDPOINT = "https://overpass-api.de/api/interpreter"
BUSCHENSCHANK_QUERY = """
    area["name"="Österreich"]->.boundaryarea;
    (
        node(area.boundaryarea)["cuisine"~"buschenschank"];
        way(area.boundaryarea)["cuisine"~"buschenschank"];
        relation(area.boundaryarea)["cuisine"~"buschenschank"];
        node(area.boundaryarea)["cuisine"~"heuriger"];
        way(area.boundaryarea)["cuisine"~"heuriger"];
        relation(area.boundaryarea)["cuisine"~"heuriger"];
    );
    out center meta;
""".replace(
    "\n", ""
)

# Secret key generation functions
secret_key_fn = os.path.join(os.path.dirname(__file__), "secret.key")


def create_secret_key():
    import random
    import string

    return "".join([random.SystemRandom().choice(string.printable) for i in range(50)])


def create_secret_key_file(secret_key):
    with open(secret_key_fn, "w") as f:
        f.write(secret_key)
    return secret_key


def load_secret_key_file():
    with open(secret_key_fn, "r") as f:
        # Read one byte more to check content length
        skey = f.read(51)
        if len(skey) != 50:
            raise ValueError("Content of secret_key file is wrong")
        return skey


if os.path.exists(secret_key_fn):
    logger.info("Load secret key from file")
    SECRET_KEY = load_secret_key_file()
else:
    logger.warning("Unable to import SECRET_KEY generating a new one")
    SECRET_KEY = create_secret_key_file(create_secret_key())
