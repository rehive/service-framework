import os

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration


# Sentry
# ---------------------------------------------------------------------------------------------------------------------
sentry_sdk.init(
    os.environ.get('SENTRY_DSN_KEY'),
    integrations=[DjangoIntegration()],
    environment=os.environ.get('SENTRY_ENV')
)