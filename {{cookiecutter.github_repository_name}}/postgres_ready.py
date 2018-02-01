import os
from time import sleep
import psycopg2

config = {
    'host': os.environ.get('POSTGRES_HOST', 'postgres'),
    'user': os.getenv("POSTGRES_USER", "postgres"),
    'password': os.environ.get('POSTGRES_PASSWORD', ''),
    "dbname": os.getenv("POSTGRES_DB", "postgres"),
}


def pg_isready(**kwargs):
    try:
        psycopg2.connect(**kwargs)
        print("Postgres is ready!")
        return True
    except psycopg2.OperationalError as exc:
        print(exc)
        return False


while not pg_isready(**config):
    print('Postgres not ready. Waiting...')
    sleep(1)
