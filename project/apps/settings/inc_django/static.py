import os

from apps.settings.common import BASE_DIR


STATIC_ROOT = os.path.join(BASE_DIR, '../static/')
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, './apps/assets/')]
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]
