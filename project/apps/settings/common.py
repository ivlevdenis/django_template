import os
import environ

env = environ.Env(
    ALLOWED_HOSTS=(list, []),
    DEBUG=(bool, False),
    SECRET_KEY=(str, ''),
    SENTRY_DSN=(str, ''),
)

DEBUG = env('DEBUG')
SECRET_KEY = env('SECRET_KEY')

ADMINS = [env('ADMINS', tuple, ('Admin', 'root@localhost'))]
ALLOWED_HOSTS = env('ALLOWED_HOSTS')
BASE_DIR = os.path.join(os.path.dirname(__file__), '..', '..')
INTERNAL_IPS = ['127.0.0.1']
FIRST_DAY_OF_WEEK = 1
ROOT_URLCONF = 'apps.urls'

# Django settings
from .inc_django.applications import *  # noqa
from .inc_django.auth import *  # noqa
from .inc_django.caches import *  # noqa
from .inc_django.databases import *  # noqa
from .inc_django.email import *  # noqa
from .inc_django.languages import *  # noqa
from .inc_django.logging import *  # noqa
from .inc_django.media import *  # noqa
from .inc_django.middleware import *  # noqa
from .inc_django.security import *  # noqa
from .inc_django.session import *  # noqa
from .inc_django.static import *  # noqa
from .inc_django.templates import *  # noqa
from .inc_django.tz import *  # noqa

# 3-rd party tools
from .inc_other.celery_config import *  # noqa
from .inc_other.constance import *  # noqa
from .inc_other.cors import *  # noqa
from .inc_other.debug_toolbar import *  # noqa
from .inc_other.drf import *  # noqa
from .inc_other.jwt import *  # noga
from .inc_other.sentry_config import *  # noqa
from .inc_other.swagger import *  # noqa
from .inc_other.watchman import *  # noqa
