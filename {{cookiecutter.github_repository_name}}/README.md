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
and relatelive simple was to use virtual environments. 
The [The Hitchhiker’s Guide to Python!](http://docs.python-guide.org/en/latest/) has a nice tutorial for setting up [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/#lower-level-virtualenv) and [virtualenvwrapper](http://docs.python-guide.org/en/latest/dev/virtualenvs/#virtualenvwrapper)

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
./manage.py migrate
```

**Setup all the static files**
```
./manage.py collectstatic
```

## Local development
**Run the postgres container in the background (if not already running)**
```
docker-compose up -d postgres
```

**Run the webserver**
```
./manage.py runserver
```

## Deployments
Deployements are automated using Travis CI and Heroku.
Pushes to the master branch will trigger a build via Travis. Once the build passes,
Travis will deploy the branch to Heroku.

- Make sure your project is on github
- Sign up on (travis.org)[https://travis-ci.org/] if you repo is open source or
(travis.com)[https://travis-ci.com/] for private repos
- Sync your account
- Turn on the switch for your repository
- Sign up on (Heroku)[https://signup.heroku.com/]
- Run the following command locally to initialize your project
```
heroku create {{cookiecutter.github_repository_name}} --remote prod && \
heroku addons:create heroku-postgresql:hobby-dev --app {{cookiecutter.github_repository_name}} && \
heroku config:set \
    DJANGO_SECRET=`openssl rand -base64 32` \
    DJANGO_SETTINGS_MODULE="config.settings" \
    --app {{cookiecutter.github_repository_name}}
```
- Encrypt your Heroky credentials and allow Travis to view them for deployments
```
travis encrypt HEROKU_AUTH_TOKEN="$(heroku auth:token)" --add
``` 
- Commit and push the changes to master to trigger the first build