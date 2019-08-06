from .common import *  # noqa

SECRET_KEY = 'not-a-valid-secret-key'
DATABASES = {
    'default': env.db(default='postgres://{{ project_name }}:{{ project_name }}@127.0.0.1:5432/{{ project_name }}'),
}
CACHES = {
    'default': env.cache(default='redis://127.0.0.1/0'),
    'session': env.cache(default='redis://127.0.0.1/1'),
}
