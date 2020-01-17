# Introduction

This is the documentation for Django-Bridger, an attempt to close the gap between a Django-Based REST Backend and a JS-Based Frontend, such as React.

The main concept is to leverage pre-request `OPTIONS` requests where all information about the upcoming request are provided.
These information can afterwards be used in order to build a frontend automatically.


# Installation

To install Django-Bridger use pip:

    pip install django-bridger

Afterwards add bridger to the project by:

```python
INSTALLED_APPS = [
    ...
    "bridger",
    ...
]
```

# Install Development Environment

To use Django-Bridger in a local development environment we first need to clone the repository from GitHub:

    git clone git@github.com:intellineers/django-bridger.git

To install all needed packages, call `pipenv install --dev`.
Next we need to setup a Postgres Database. This can either be done manually or through Docker and Docker-Compose.
For convinience a `docker-compose.yml` is supplied to easily setup the Postgres Database. In order to have persistant
data, the folder `DockerVolumes` has to be created in the Home directory. Calling `pipenv run start_db` will pull
the latest Postgres Image and setup the Postgres Database. Call `pipenv run psql` to open a psql session to create
a database. Last create a `.env` file and supply the database url in the following format:

    DATABASE_URL=postgres://root:root@localhost:5432/<DATABASE_NAME>

Before running the server we need to migrate the data by calling `pipenv run ./manage.py migrate` and then `pipenv run local`
to start the development server.

# Testing

In order to run the test-suite, either call:

    export DATABASE_URL=postgres://root:root@localhost:5432/<DATABASE_NAME> tox

or:

    pipenv run tox

You have to ensure that the DATABASE_URL is set as an environment variable, because it is passed down through tox.