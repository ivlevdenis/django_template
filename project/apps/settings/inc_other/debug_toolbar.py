# https://github.com/jazzband/django-debug-toolbar
DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': 'apps.settings.inc_other.debug_toolbar.show_toolbar',
}


def show_toolbar(request):
    return True
