from apps.settings.common import env


TIME_ZONE = env('TIME_ZONE', str, 'Europe/Moscow')
USE_TZ = True
