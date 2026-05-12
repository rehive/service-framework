import os
from logging import getLogger


logger = getLogger('django')


if os.environ.get('SKIP_TASK_QUEUE') in ['True', 'true', True]:
    logger.info('Task Queues Disabled')
    CELERY_TASK_ALWAYS_EAGER = True
    CELERY_TASK_EAGER_PROPAGATES = True
else:
    logger.info('Task Queues Enabled')

CELERY_IMPORTS = ("{{ cookiecutter.module_name }}.models",)

CELERY_ENABLE_UTC = True
CELERY_TIMEZONE = "UTC"

CELERY_TASK_CREATE_MISSING_QUEUES = True
CELERY_WORKER_PREFETCH_MULTIPLIER = 5
CELERY_BROKER_CONNECTION_TIMEOUT = 3
CELERY_BROKER_TRANSPORT_OPTIONS = {
    "max_retries": 3,
    'interval_step': 0,
    'interval_max': 0
}

CELERY_TASK_SERIALIZER = 'msgpack'
CELERY_ACCEPT_CONTENT = ['msgpack', 'json']

project_id = os.environ.get('CELERY_ID', 'local')

# General queue for unassigned tasks.
general_queue = '-'.join(('general', project_id))
# Queue for processing Platform webhook event tasks.
platform_webhook_queue = '-'.join(('platform-webhook', project_id))

# Assign all tasks to the default queue by default.
CELERY_TASK_DEFAULT_QUEUE = general_queue

# Specify what queues individual tasks should be assigned to.
CELERY_TASK_ROUTES = {
    # Platform webhook tasks.
    '{{ cookiecutter.module_name }}.tasks.process_platform_webhook': {
        'queue': platform_webhook_queue
    },
}

CELERY_BROKER_URL = 'amqp://{user}:{password}@{hostname}/{vhost}'.format(
    user=os.environ.get('RABBITMQ_USER', 'guest'),
    password=os.environ.get('RABBITMQ_PASSWORD', 'guest'),
    hostname="%s:%s" % (
        os.environ.get('RABBITMQ_HOST', 'rabbitmq'),
        os.environ.get('RABBITMQ_PORT', '5672')
    ),
    vhost=os.environ.get('RABBITMQ_VHOST', '/'),
)

CELERY_IGNORE_RESULT = True

CELERY_BEAT_SCHEDULE = {

}
