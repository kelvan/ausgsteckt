import os
import logging

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(os.path.dirname(BASE_DIR), 'public')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'el5m47jko&tz)i-qw_@b5wp=6ots)o3qcv^ekrceu$fcm1@jll'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'flat_responsive',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'easy_thumbnails',
    'pipeline',
    'ausgsteckt',
    'buschenschank',
    'data_quality'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ausgsteckt.urls'

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
                'buschenschank.context_processors.region_list',
            ],
        },
    },
]

WSGI_APPLICATION = 'ausgsteckt.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'ausgsteckt'
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'de-at'

ugettext = lambda s: s
LANGUAGES = (
    ('de', ugettext('German')),
    ('en', ugettext('English')),
)

LOCALE_PATHS = (os.path.join(BASE_DIR, 'locale'),)
TIME_ZONE = 'Europe/Vienna'
USE_I18N = True
USE_L10N = False
USE_TZ = True


STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(DATA_DIR, 'media')
STATIC_ROOT = os.path.join(DATA_DIR, 'static')

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'pipeline.finders.CachedFileFinder',
)
STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

PIPELINE = {
    'PIPELINE_ENABLED': True,
    'JS_COMPRESSOR': 'pipeline.compressors.NoopCompressor',
    'JAVASCRIPT': {
        'map': {
            'source_filenames': (
                'node_modules/leaflet/dist/leaflet.js',
                'node_modules/leaflet-providers/leaflet-providers.js',
                'node_modules/leaflet-plugins/control/Permalink.js',
                'node_modules/leaflet-plugins/control/Permalink.Marker.js',
                'node_modules/leaflet-plugins/control/Permalink.Layer.js',
                'node_modules/leaflet-plugins/control/Permalink.Overlay.js',
                'js/leaflet.markercluster.js',
                'js/buschenschank/map.js',
            ),
            'output_filename': 'js/map.js'
        },
        'libs': {
            'source_filenames': (
                'node_modules/jquery/dist/jquery.min.js',
                'node_modules/popper.js/dist/umd/popper.js',
                'node_modules/bootstrap/dist/js/bootstrap.min.js',
            ),
            'output_filename': 'js/libs.js',
        },
    },
    'CSS_COMPRESSOR': 'pipeline.compressors.NoopCompressor',
    'STYLESHEETS': {
        'main': {
            'source_filenames': (
                'css/main.css',
            ),
            'output_filename': 'css/main.css'
        },
        'map': {
            'source_filenames': (
                'css/buschenschank/map.css',
                'node_modules/leaflet/dist/leaflet.css',
                'css/MarkerCluster.css',
                'css/MarkerCluster.Default.css',
            ),
            'output_filename': 'css/map.css',
        },
        'libs': {
            'source_filenames': (
                'node_modules/bootstrap/dist/css/bootstrap.min.css',
                'node_modules/font-awesome/css/font-awesome.min.css',
            ),
            'output_filename': 'css/libs.css',
        }
    }
}

THUMBNAIL_ALIASES = {
    '': {
        'details': {'size': (150, 0), 'crop': False},
        'dropdown': {'size': (15, 15), 'crop': False},
        'list': {'size': (25, 25), 'crop': False},
    },
}

# OSM settings

OVERPASS_ENDPOINT = 'https://overpass-api.de/api/interpreter'
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
""".replace('\n', '')

## Secret key generation functions
secret_key_fn = os.path.join(os.path.dirname(__file__), 'secret.key')


def create_secret_key():
    import random
    import string

    return ''.join(
        [random.SystemRandom().choice(string.printable) for i in range(50)]
    )


def create_secret_key_file(secret_key):
    with open(secret_key_fn, 'w') as f:
        f.write(secret_key)
    return secret_key


def load_secret_key_file():
    with open(secret_key_fn, 'r') as f:
        # Read one byte more to check content length
        skey = f.read(51)
        if len(skey) != 50:
            raise ValueError('Content of secret_key file is wrong')
        return skey


if os.path.exists(secret_key_fn):
    logger.info('Load secret key from file')
    SECRET_KEY = load_secret_key_file()
else:
    logger.warning('Unable to import SECRET_KEY generating a new one')
    SECRET_KEY = create_secret_key_file(create_secret_key())
