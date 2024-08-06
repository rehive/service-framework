# {{cookiecutter.app_name}}

{{cookiecutter.description}}

## Prerequisites

Make sure you have the following installed
- Docker
- Travis CLI
- Heroku CLI

## Local setup

**Create a vitual environment and activate it**

If you are new to this, virtualenv with virtualenvwrapper is a straight forward
and relatively simple was to use virtual environments.
The [The Hitchhiker's Guide to Python!](http://docs.python-guide.org/en/latest/) has a nice tutorial for setting up [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/#lower-level-virtualenv) and [virtualenvwrapper](http://docs.python-guide.org/en/latest/dev/virtualenvs/#virtualenvwrapper)

Else, with [conda](https://docs.conda.io/en/latest/):
```
conda create -n service-test python=3.10
```

**Install requirements**
```
pip install -r requirements.txt
```

**Run the postgres container in the background**
```
docker-compose up -d postgres
```

Run `docker ps` to make sure your container is running.

**Migrate all the data to the database**
```
python src/manage.py migrate
```

**Run the webserver to see if everything is working**
```
python src/manage.py runserver
```

## Local development

**Run the postgres container in the background (if not already running)**
```
docker-compose up -d postgres
```

**Run the webserver**
```
python src/manage.py manage.py runserver
```

## Deployments

### Initial setup

Install rdeploy
```
pip install rdeploy
```
Gcloud login
```
glcoud auth login
```
Create namespace
```
rdeploy create-namespace staging
```
Tag the release
```
rdeploy git-release patch staging
```
Build the docker image
```
rdeploy cloudbuild staging 0.0.1
```
Upload secrets
```
rdeploy upload-secrets staging local/path/to/staging.env
```
Install
```
rdeploy install staging
```

### Deploying

Deploy to staging
```
deploy git-release patch staging
rdeploy cloudbuild staging <tag>
rdeploy upgrade staging <tag>
```

