# AUTHENTICATION_BACKENDS
AUTH_USER_MODEL = 'accounts.User'
LOGIN_URL = '/admin/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
# AUTH_PASSWORD_VALIDATORS

MIN_PASSWORD_LENGTH = 12

# Backends
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'guardian.backends.ObjectPermissionBackend',
)
