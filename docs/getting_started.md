### Installation

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

### Install Development Environment

#### Cloning the repository

    git clone git@github.com:intellineers/django-bridger.git

#### Installing system dependencies

* [Poetry](https://python-poetry.org/docs/#installation)
    * For pypi depenendency management / package building
* [Docker](https://docs.docker.com/get-docker/)
    * For running external containerized services
* [Docker-Compose](https://docs.docker.com/compose/install/)
    * For orchestrating containerized services


#### Setup environment variables

The url for the database has to be stored as a environment variable:

    export DATABASE_URL=postgres://root:root@localhost:5432/bridger

!!! hint
    The management of environment variables is not automatically handled in poetry (opposed to pipenv), therefore you as a developer has to take care of this.  
    **Tip:** Use [direnv](https://direnv.net/) and store the environment variables in a `.envrc` file.

#### Setup initial system

In order to make the system work the following steps have to be taken:

1. Get the latest version of the repository
1. Install all dependencies through poetry
1. Startup docker containers which run external services (Postgres, Redis, S3 Minio)
    * Postgres and S3 Minio are setup to have persistant data stored in the folder `~/DockerVolumes/`
1. Create a database
1. Migrate the database
1. **Optionally** insert fixtures into the database

To ease and speedup the process of setting up the development environment the last 6 steps can be done automatically by running the following script

    ./scripts/startup

### Useful Scripts

#### Development Server

Two development servers are available, one for the web-worker:

    ./scripts/dev-server

The other one is a celery consumer:

    ./scripts/celery


#### Testing

In order to run all tests with pytest:

    ./scripts/pytest

If you want to run all tests without the pytest-cache:

    ./scripts/pytest_full

If you want to deploy changes, you need to make sure that running the tests in an isolated environment with tox do not fail:

    poetry run tox


#### Documentation

The documentation is available locally under `http://localhost:8000`:

    ./scripts/docs

#### Interactive Shell and Notebooks

The shell with a preloaded django environment is available under:

    ./scripts/django_shell

The same django environment is also available as a notebook:

    ./scripts/notebook

#### Database (PSQL)

Quick access to a psql shell:

    ./scripts/psql

#### Misc.

Sort all python imports:

    ./scripts/isort

