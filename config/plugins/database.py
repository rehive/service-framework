import os

if os.environ.get('POSTGRES_PORT'):
    POSTGRES_PORT = os.environ.get('POSTGRES_PORT')
else:
    POSTGRES_PORT = 5432

if os.environ.get('POSTGRES_HOST'):
    POSTGRES_HOST = os.environ.get('POSTGRES_HOST')
else:
    POSTGRES_HOST = 'postgres'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('POSTGRES_DB', 'postgres'),
        'USER': os.environ.get('POSTGRES_USER', 'postgres'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'postgres'),
        'HOST': POSTGRES_HOST,
        'PORT': POSTGRES_PORT,
        'OPTIONS': {
            'connect_timeout': 25,
        }
    }
}
