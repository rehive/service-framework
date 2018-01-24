# {{cookiecutter.app_name}}
{{cookiecutter.description}}

## Local setup
Build the required containers
```
docker-compose build
```

Run the containers in the background
```
docker-compose up -d
```

Migrate all the data to the database
```
docker exec -it {{cookiecutter.app_name}}_webapp_1 ./manage.py migrate
```

Setup all the static files
```
docker exec -it {{cookiecutter.app_name}}_webapp_1 ./manage.py collectstatic
```

## Local development
Run the containers in the background
```
docker-compose up -d
```

When done with development, if you would like to stop the containers running
```
docker stop {{cookiecutter.app_name}}_webapp_1
```

When commands need to be run on the webserver, such as running new migrations, if the webserver is running in the background the following command can be used to execute commands on the container
```
docker exec -it {{cookiecutter.app_name}}_webapp_1 {{command}}
```
