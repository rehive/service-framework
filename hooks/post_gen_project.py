import os
import random
import string


PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)


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
        string.ascii_letters + string.digits + string.punctuation
    ) for i in range(50))

    file_data = file_data.replace('replace_django_secret', secret_key, 1)

    with open(env_file, 'w') as _file:
        _file.write(file_data)


def remove_travis_files():
    """Remove associated Travis CI files"""
    file_names = ['.travis.yml']
    remove_files(file_names)


def remove_heroku_files():
    """Remove associated Heroku files"""
    file_names = ['Procfile']
    remove_files(file_names)


# Create django secret
make_django_secret()

# Check use travis
if '{{cookiecutter.use_travis_ci}}' == 'n':
    remove_travis_files()

# Check use Heroku
if '{{cookiecutter.use_heroku}}' == 'n':
    remove_heroku_files()
