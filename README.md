<p align="center">
  <img width="64" src="https://avatars2.githubusercontent.com/u/22204821?s=200&v=4" alt="Rehive Logo">
  <h1 align="center">Service Framework</h1>
  <p align="center">A framework that can be used as a base to build services on Rehive</p>
</p>


## Features
- Python 3.6
- Django 1.11
- [Django Rest Framework](http://www.django-rest-framework.org/) integration
- PostgreSQL 9.6
- Running in a self-contained [Docker](https://www.docker.com/) containers
- Automatic deployments to Heroku
 

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
 cookiecutter gh:rehive/service-framework
 ```