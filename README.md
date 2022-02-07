<p align="center">
  <img width="64" src="https://avatars2.githubusercontent.com/u/22204821?s=200&v=4" alt="Rehive Logo">
  <h1 align="center">Service Framework</h1>
  <p align="center">A framework that can be used as a base to build services on Rehive</p>
</p>


## Features

- Python 3.10
- Django 4.0.1
- [Django Rest Framework](http://www.django-rest-framework.org/) integration
- PostgreSQL 13.0
- Running in a self-contained [Docker](https://www.docker.com/) containers
- Automatic deployments to Heroku using Travis CI

**Notes:**
- The service framework has been set up to work with Travis CI and Heroku for automatic
deployments. Travis CI is not a requirement for deployments to Heroku to work and is used 
as a method of automation.
- If you choose not to use Heroku, you will have to set up deployments yourself.
 

## Getting started

Install [cookiecutter](https://github.com/audreyr/cookiecutter). Further documentation for installation can be found [here](https://cookiecutter.readthedocs.io/en/latest/installation.html#install-cookiecutter).
```
# Pip
pip install --user cookiecutter

# Homebrew (Mac OS X only):
brew install cookiecutter

# Debian/Ubuntu:
sudo apt-get install cookiecutter
```

Create your project using the cookie cutter template
```
# SSH
cookiecutter git@github.com:rehive/service-framework.git

# HTTPS
cookiecutter https://github.com/rehive/service-framework.git
```

Run through the command promts and fill in your project details.
Follow the instructions in your newly cloned project for how to setup local development.
