from datetime import timedelta
import os
from logging import getLogger

from celery.schedules import crontab


logger = getLogger('django')

if os.environ.get('SKIP_TASK_QUEUE') in ['True', 'true', True]:
    logger.info('Task Queues Disabled')
    CELERY_TASK_ALWAYS_EAGER = True
else:
    logger.info('Task Queues Enabled')

CELERY_IMPORTS = ("conversion.models",)

CELERY_ENABLE_UTC = True
CELERY_TIMEZONE = "UTC"

CELERY_TASK_CREATE_MISSING_QUEUES = True
CELERY_WORKER_PREFETCH_MULTIPLIER = 15
CELERY_BROKER_CONNECTION_TIMEOUT= 10.0

CELERY_TASK_SERIALIZER = 'msgpack'
CELERY_ACCEPT_CONTENT = ['msgpack', 'json']

project_id = os.environ.get('CELERY_ID', 'local')

default_queue = '-'.join(('general', project_id))
CELERY_TASK_DEFAULT_QUEUE = default_queue

CELERY_TASK_ROUTES = {
    '{{cookiecutter.module_name}}.tasks.process_transaction_initiated_webhooks': {'queue': default_queue},
    '{{cookiecutter.module_name}}.tasks.process_platform_webhook': {'queue': default_queue},
}

# RabbitMQ
CELERY_BROKER_URL = 'amqp://{user}:{password}@{hostname}/{vhost}'.format(
    user=os.environ.get('RABBITMQ_USER', 'guest'),
    password=os.environ.get('RABBITMQ_PASSWORD', 'guest'),
    hostname="%s:%s" % (
        os.environ.get('RABBITMQ_HOST','rabbitmq'),
        os.environ.get('RABBITMQ_PORT','5672')
        ),
    vhost=os.environ.get('RABBITMQ_VHOST', '/'))

CELERY_IGNORE_RESULT = True

# Include any recurring tasks here
CELERY_BEAT_SCHEDULE = {}
