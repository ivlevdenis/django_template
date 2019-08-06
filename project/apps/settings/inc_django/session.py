SESSION_CACHE_ALIAS = 'session'
SESSION_COOKIE_AGE = 60 * 60 * 24 * 1  # 1 days
SESSION_COOKIE_SECURE = False
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'
