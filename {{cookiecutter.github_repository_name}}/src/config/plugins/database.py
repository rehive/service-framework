import os

options = {
        'connect_timeout': 25,
    }

if not os.environ.get('POSTGRES_SSL_DISABLE') in [True, "True", 'true']:
    options['sslmode'] = 'require'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB', 'postgres'),
        'USER': os.environ.get('POSTGRES_USER', 'postgres'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'postgres'),
        'HOST': os.environ.get('POSTGRES_HOST', 'localhost'),
        'PORT': os.environ.get('POSTGRES_PORT', '5432'),
        'OPTIONS': options
    }
}

if os.environ.get('DOCKER_NETWORK', False) in [True, 'True', 'true']:
    DATABASES['default']['PORT'] = '5432'
