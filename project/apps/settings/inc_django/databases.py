from apps.settings.common import env


DATABASES = {
    'default': env.db(default='postgres://django:django@db:5432/django'),
}
