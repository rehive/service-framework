import os

# Check if debug variable is there to determine whether loaded
env_vars_loaded = os.environ.get('DEBUG', '')

# fallback for when env variables are not loaded:
if not env_vars_loaded:
    try:
        print('Loading keys from file...')
        current_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        file_path = os.path.join(current_directory, '../.env')
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

    os.environ["POSTGRES_HOST"] = os.environ.get('LOCAL_POSTGRES_HOST', 'localhost')
    os.environ["POSTGRES_PORT"] = os.environ.get('LOCAL_POSTGRES_REMOTE_PORT', '5432')

# Add all project configurations that are stored in env variables:

# config
DEBUG = os.environ.get('DEBUG', '') in ['True', True, 'true']

# secrets
SECRET_KEY = os.environ.get('DJANGO_SECRET', 'local')
