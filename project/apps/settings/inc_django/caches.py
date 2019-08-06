from apps.settings.common import env

CACHES = {
    'default': env.cache(default='redis://redis/0'),
    'session': env.cache('CACHE_SESSION_URL', default='redis://redis/1'),
}
