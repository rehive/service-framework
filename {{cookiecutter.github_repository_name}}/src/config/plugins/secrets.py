import os

# Check if debug variable is there to determine whether loaded
env_vars_loaded = os.environ.get('COMPOSE_FILE')

# fallback for when env variables are not loaded:
if not env_vars_loaded:
    try:
        print('Loading keys from file...')
        current_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        parent_directory = os.path.split(current_directory)[0]
        parent_directory = os.path.split(parent_directory)[0]
        file_path = os.path.join(parent_directory, './.env')
        print(file_path)
        with open(file_path, 'r') as f:
            output = f.read()
            output = output.split('\n')

        for var in output:
            if var and not var.startswith('#'):
                k, v = var.split('=', maxsplit=1)
                os.environ.setdefault(k, v)
    except FileNotFoundError:
        print('environmental variables file not found: {}'.format(file_path))
        pass

    local_postgres_host = os.environ.get('LOCAL_POSTGRES_HOST')
    local_postgres_port = os.environ.get('LOCAL_POSTGRES_PORT')
    postgres_host = os.environ.get('POSTGRES_HOST')
    postgres_port = os.environ.get('POSTGRES_PORT')

    if local_postgres_host:
        os.environ["POSTGRES_HOST"] = local_postgres_host

    if local_postgres_port:
        os.environ["POSTGRES_PORT"] = local_postgres_port

# Add all project configurations that are stored in env variables:

# config
DEBUG = os.environ.get('DEBUG', '') in ['True', True, 'true']

# secrets
SECRET_KEY = os.environ.get('DJANGO_SECRET', 'local')
