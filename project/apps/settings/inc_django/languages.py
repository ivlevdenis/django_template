import os
from django.utils.translation import ugettext_lazy as _
from apps.settings.common import BASE_DIR


USE_I18N = True
USE_L10N = True
LANGUAGE_CODE = 'ru'
LANGUAGES = (
    ('ru', _('Russian')),
)
LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale/')]
