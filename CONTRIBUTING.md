# Contributing guide
Welcome! If you'd like to contribute to fakester (or run it yourself), you came to
right place. Hopefully, everything noteworthy is mentioned, but if you still have
some questions after reading it all, don't hesitate to open up a [new discussion].

## Tools used
**Language:** [Python 3.11.2][python]  
**Web framework:** [Django]  
**Database:** [PostgreSQL]  
**Cache:** [Redis]  
**CI:** [GitHub Actions]  
**Error tracking:** [Sentry]  
**Testing:** [pytest], [nox]  
**Code style:** [black], [isort], [ruff], [interrogate]  
**Other:** [pip-tools], [Docker], [Docker Compose], Makefile  

## Code style
All code is formatted with the amazing `black`, `isort` and `ruff` tools via
`make format` helper command.

## Tests
Tests are written with help of [pytest] and run via [nox] (alongside other checks).
To run the test suite yourself, all you need to do is remember to have the database
running locally and run:

```console
$ # Install nox
$ python -m pip install nox -c requirements/constraints.txt
$ # Run nox
$ make test
```

## Running locally
The easiest way run fakester locally is to install [Docker] and run:

```console
$ # Build Docker images
$ make docker-build
$ # Run Docker compose stack
$ make docker-run
```

If everything went well, fakester should be available at http://localhost:8000/

Alternatively, you can also run fakester without [Docker], but you need to have
[PostgreSQL] and [Redis] installed and running locally:

```console
$ # Create a Python virtualenv
$ python3 -m venv venv
$ source venv/bin/activate
$ # Install dependencies
$ make install-dev
$ # Run the app
$ make run
```

### Migrations
If you're setting up the app for the first time (or some database model changes were
introduced since you last used it), you need to apply the database migrations:

```console
$ make apply-migrations
```

### Configuration
All configurable settings are loaded from environment variables and a local `.env`
file (in that order). Note that when running locally through Docker Compose, you
need to restart the app for it to pick up the changes.

Available settings:

```
# App environment. Should be set to one of: "local" or "production"
# Default: "local"
ENVIRONMENT='production'

# Django's secret key. Should be kept private and needs to be set on a non-local enviroment.
# Defualt: "CHANGE_ME"
# Docs: https://docs.djangoproject.com/en/4.1/ref/settings/#secret-key
SECRET_KEY='THIS_IS_A_VERY_SECRET_KEY'

# Controls Django's debug mode. Can't be enabled on a non-local enviroment.
# Docs: https://docs.djangoproject.com/en/4.1/ref/settings/#debug
DEBUG='True'

# Comma separated list of allowed hosts
# Default: None
# Docs: https://docs.djangoproject.com/en/4.1/ref/settings/#allowed-hosts
ALLOWED_HOSTS='*'

# Database URL
# Default: "postgres://postgres@localhost/fakester"
# Docs: https://github.com/jazzband/dj-database-url#url-schema
DATABASE_URL='postgres://fakester:fakester@localhost:54320/fakester'

# Redis URL
# Default: "redis://localhost:6379"
# Docs: https://docs.djangoproject.com/en/4.1/topics/cache/#redis
REDIS_URL='redis://redis:6379'

# Comma separated list of linked domains. Used to generate a list of all redirect fakester links
# Default: None
AVAILABLE_DOMAINS='example.com,foo.bar'

# Sentry DSN. If not set, Sentry integration will be disabled.
# Default: None
# Docs: https://docs.sentry.io/platforms/python/#configure
SENTRY_DSN='https://*****@*****.ingest.sentry.io/*****'
```

## Makefile
Available `make` commands:

```console
$ make help
install                                   Install app dependencies
install-dev                               Install app dependencies (including dev)
pip-compile                               Compile requirements files
upgrade-package                           Upgrade Python package (pass "package=<PACKAGE_NAME>")
upgrade-all                               Upgrade all Python packages
run                                       Run the app
create-migration                          Create Django migration (pass "name=<MIGRATION_NAME>")
apply-migrations                          Apply Django migrations
format                                    Format code
test                                      Run the test suite
docker-build                              Build Docker compose stack
docker-run                                Run Docker compose stack
docker-stop                               Stop Docker compose stack
docker-shell                              Run bash inside dev Docker image
clean                                     Clean dev artifacts
help                                      Show help message
```


[black]: https://black.readthedocs.io/
[django]: https://www.djangoproject.com/
[docker]: https://www.docker.com/
[docker compose]: https://docs.docker.com/compose/
[github actions]: https://github.com/features/actions
[interrogate]: https://github.com/econchick/interrogate
[isort]: https://github.com/timothycrosley/isort
[new discussion]: https://github.com/pawelad/fakester/discussions/new/choose
[nox]: https://nox.readthedocs.io/
[pip-tools]: https://github.com/jazzband/pip-tools
[postgresql]: https://www.postgresql.org/
[pytest]: https://pytest.org/
[python]: https://www.python.org/
[redis]: https://redis.io/
[ruff]: https://github.com/charliermarsh/ruff
[sentry]: https://sentry.io/
