import os
import dj_database_url

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('POSTGRES_DB', 'postgres'),
        'USER': os.environ.get('POSTGRES_USER', 'postgres'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'postgres'),
        'HOST': os.environ.get('LOCAL_POSTGRES_HOST', 'localhost'),
        'PORT': os.environ.get('LOCAL_POSTGRES_REMOTE_PORT', '5432')
    }
}

DATABASES['default'].update(
    dj_database_url.config(conn_max_age=500)
)
