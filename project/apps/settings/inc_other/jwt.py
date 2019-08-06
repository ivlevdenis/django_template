from datetime import timedelta

JWT_AUTH = {'JWT_EXPIRATION_DELTA': timedelta(seconds=900), 'JWT_ALLOW_REFRESH': True}

