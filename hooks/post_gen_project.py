import os
import random
import string
import shutil


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


def remove_heroku_travis_files():
    """
    Remove associated Heroku and TravisCI files.
    All k8s setup files are located in etc/
    """
    file_names = [
        '.travis.yml', 'Procfile', 'docker-compose.yml', 'Dockerfile',
        'postgres_ready.py'
    ]
    for file_name in file_names:
        file_path = os.path.join(PROJECT_DIRECTORY, file_name)
        if os.path.exists(file_path):
            os.remove(file_path)
            assert file_path not in os.listdir(PROJECT_DIRECTORY)


def remove_gcould_k8s_files():
    """
    Move all files out of src/ to the PROJECT_DIR for heroku and travis 
    deployment setup.
    """
    os.rmdir(os.path.join(PROJECT_DIRECTORY, 'etc'))
    assert 'src' in os.listdir(PROJECT_DIRECTORY)
    files = os.listdir(os.path.join(PROJECT_DIRECTORY, 'src'))
    for f in files:
        shutil.move(f, PROJECT_DIRECTORY)
    assert 'manage.py' in os.listdir(PROJECT_DIRECTORY)
    os.rmdir(os.path.join(PROJECT_DIRECTORY, 'src'))


# Create django secret
make_django_secret()

# Check use travis
if '{{cookiecutter.server_infrastructure}}' == 'Heroku + TravisCI':
    remove_gcould_k8s_files()
elif '{{cookiecutter.server_infrastructure}}' == 'GCloud + Kubernetes':
    remove_heroku_travis_files()
