from apps.settings.common import env

# https://github.com/ottoyiu/django-cors-headers
CORS_ORIGIN_ALLOW_ALL = env('CORS_ORIGIN_ALLOW_ALL', bool, False)
CORS_ORIGIN_WHITELIST = env('CORS_ORIGIN_WHITELIST', list, [])
CSRF_TRUSTED_ORIGINS = CORS_ORIGIN_WHITELIST
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = (
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'access-control-allow-origin',
)
