# LOGGING
# ------------------------------------------------------------------------------
import logging
logger = logging.getLogger('django')


# IMPORTS
# ------------------------------------------------------------------------------
from django.apps import AppConfig


# APP CONFIG
# ------------------------------------------------------------------------------
class ConfigAppConfig(AppConfig):
    name = 'config'

    def ready(self):
        import config.schema
