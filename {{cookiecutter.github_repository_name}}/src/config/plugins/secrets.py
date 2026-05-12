import os


# Check if env vars are already loaded to determine whether to fall back to .env file.
env_vars_loaded = os.environ.get('DJANGO_DEBUG', '')

# Fallback for when env variables are not loaded:
if not env_vars_loaded:
    try:
        current_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        parent_directory = os.path.split(current_directory)[0]
        parent_directory = os.path.split(parent_directory)[0]

        file_path = os.path.join(parent_directory, './.env')
        with open(file_path, 'r') as f:
            output = f.read()
            output = output.split('\n')

        for var in output:
            if var:
                k, v = var.split('=', maxsplit=1)
                os.environ.setdefault(k, v)
    except FileNotFoundError:
        pass

# Add all project configurations that are stored in env variables:

# config
DEBUG = os.environ.get('DJANGO_DEBUG', '') in ['True', True, 'true']

# secrets
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
