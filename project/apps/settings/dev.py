from .common import *  # noqa

SITE_URL = 'http://localhost:8080'
ALLOWED_HOSTS = ['*']
DEBUG = True
SECRET_KEY = 'not-a-valid-secret-key'

INSTALLED_APPS += (
    'debug_toolbar',
    'rosetta',
)

MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')
