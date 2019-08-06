import sentry_sdk
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.django import DjangoIntegration

from apps.settings.common import env


sentry_sdk.init(
    dsn=env('SENTRY_DSN', str, None),
    integrations=[
        CeleryIntegration(),
        DjangoIntegration(),
    ],
)
