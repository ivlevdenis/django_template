import os
from apps.settings.common import env

EMAIL_CONFIG = env.email(default='consolemail://')
DEFAULT_FROM_EMAIL = SERVER_EMAIL = EMAIL_CONFIG.get('EMAIL_HOST_USER', '')
vars().update(EMAIL_CONFIG)
