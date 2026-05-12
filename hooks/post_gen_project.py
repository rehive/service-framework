import os
import random
import string
import shutil


PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)

USE_CELERY = "{{ cookiecutter.use_celery }}" == "yes"


def remove_files(file_names):
    for file_name in file_names:
        file_path = os.path.join(PROJECT_DIRECTORY, file_name)
        if os.path.exists(file_path):
            os.remove(file_path)


def make_django_secret():
    """
    Generate a secret key and save if to the .env file
    """
    env_file = os.path.join(PROJECT_DIRECTORY, '.env')

    with open(env_file) as _file:
        file_data = _file.read()

    secret_key = ''.join(random.SystemRandom().choice(
        string.ascii_letters + string.digits
    ) for i in range(50))

    file_data = file_data.replace('replace_django_secret', secret_key, 1)

    with open(env_file, 'w') as _file:
        _file.write(file_data)


# Create django secret
make_django_secret()

# Strip Celery scaffolding when not enabled
if not USE_CELERY:
    remove_files([
        "src/config/celery.py",
        "src/config/plugins/tasks.py",
        "src/{{ cookiecutter.module_name }}/tasks.py",
    ])
