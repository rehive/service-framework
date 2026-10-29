import os

bind = '0.0.0.0:8000'
workers = int(os.environ.get('GUNICORN_WORKERS', 4))
name = os.environ.get('PROJECT_NAME')
log_level = 'info'
log_file = '-'
accesslog = '-'
pythonpath = '/app/'
forwarded_allow_ips = '*'
# Sync workers are killed after this many seconds on one request: keep slow
# work in Celery and outbound request timeouts well inside it.
timeout = int(os.environ.get('GUNICORN_TIMEOUT', 60))
graceful_timeout = 30
