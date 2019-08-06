from apps.settings.common import env

# https://github.com/mwarkentin/django-watchman
WATCHMAN_TOKENS = env('WATCHMAN_TOKEN', str, None)
WATCHMAN_TOKEN_NAME = env('WATCHMAN_TOKEN_NAME', str, 'token')
