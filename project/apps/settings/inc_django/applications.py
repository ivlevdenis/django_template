INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'corsheaders',
    'django_filters',
    'phonenumber_field',
    'drf_yasg',
    'rest_framework',
    'watchman',
    'guardian',
    'constance',
    'constance.backends.database',

    'apps.accounts',
    'apps.web',

    'django.contrib.admin',
]
