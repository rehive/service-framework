# {{cookiecutter.app_name}}
{{cookiecutter.description}}

## Local setup
Build the required containers
```
docker-compose build
```

Run the postgres container
```
docker-compose up -d postgres
```

Migrate all the data to the database
```
./src/manage.py migrate
```

Setup all the static files
```
./src/manage.py collectstatic
```

## Local development
To run the websaerver locally, simply run
```
./src/management.py runserver
```
