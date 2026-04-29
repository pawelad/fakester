# Contributing Guide
Welcome! If you'd like to contribute to `fakester` (or run it yourself), you came
to right place. Hopefully, everything noteworthy is mentioned, but if you still
have some questions after reading it all, don't hesitate to open up a 
[new issue][github new issue].

Please also note that this project is released with a [Contributor Code of Conduct].
By participating in this project you agree to abide by its terms.

## Tools used
**Language:** [Python 3.12][python]  
**Web framework:** [Django]  
**Database:** [PostgreSQL]  
**Cache:** [Redis]  
**CI:** [GitHub Actions]  
**Error tracking:** [Sentry]  
**Testing:** [pytest], [nox]  
**Code style:** [black], [isort], [ruff], [interrogate], [yamllint]  
**Other:** [uv], [Docker], [Docker Compose], Makefile  

## Code style
All code is formatted and linted with the amazing `yamllint`, `black`, `isort` and `ruff` tools via
`make format` helper command.

## Commit messages
All commit messages and PR titles must follow the [Conventional Commits][] specification
(`<type>[optional scope]: <description>`). Common types: `feat`, `fix`, `docs`,
`refactor`, `test`, `chore`, `ci`. Breaking changes append `!` after the type/scope.

## Releases and Deployment
This project uses [release-please] for automated changelog generation and version bumping.

1. **Commit and Merge**: Just merge your PRs into `main`. The commit messages must strictly follow the Conventional Commits specification.
2. **Release PR**: A Github Action automatically opens or updates a "Release PR" named `chore: release vX.Y.Z`. This PR contains the updated `CHANGELOG.md` and version bumps.
3. **Deploy**: When you are ready to cut a new release, simply merge the Release PR. This will:
    - Tag the release in Git.
    - Build and push a new Docker image to the GitHub Container Registry.
    - Trigger a deployment webhook to Dokploy.

## Tests
Tests are written with help of [pytest] and run via [nox] (alongside other checks).
To run the test suite yourself, all you need to do is remember to have the database
running locally and run:

```console
$ make test
```

`make test` orchestrates Docker and runs the following nox sessions:

| Session             | What it does                                                                  |
|---------------------|-------------------------------------------------------------------------------|
| `tests`             | Runs `pytest` with `coverage` (group: `tests`)                                |
| `coverage_report`   | Combines and reports coverage (auto-triggered locally after `tests`)          |
| `code_style_checks` | `black --check`, `isort --check`, `ruff check`, `interrogate` (group: `lint`) |
| `type_checks`       | `mypy` (groups: `typing`, `tests`, `nox`)                                     |
| `django_checks`     | `manage.py check` + `manage.py makemigrations --check`                        |

## Running locally
The easiest way run fakester locally is to install [Docker] and run:

```console
$ # Build Docker images
$ make docker-build
$ # Run Docker compose stack
$ make docker-run
```

If everything went well, fakester should be available at http://localhost:8000/

To stop the Docker stack or run a shell inside the dev container:

```console
$ make docker-stop
$ make docker-shell
```

Alternatively, you can also run fakester without [Docker], but you need to have
[PostgreSQL] and [Redis] installed and running locally:

```console
$ # Install uv (https://docs.astral.sh/uv/getting-started/installation/)
$ curl -LsSf https://astral.sh/uv/install.sh | sh
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

If you changed a Django model, create a new migration before applying it:

```console
$ make create-migration name=<descriptive_name>
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
# Default: A randomly generated secret key (only in "local" environment)
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

## Dependencies
Dependencies are managed with [uv]. Runtime dependencies go under `[project].dependencies`
in `pyproject.toml`. Everything else (testing, linting, typing, docs) belongs in the
appropriate `[dependency-groups]` group (`tests`, `lint`, `typing`, `docs`, `nox`).

After adding or changing a dependency, regenerate the lockfile:

```console
$ make lock
```

To upgrade a single package or all packages:

```console
$ make upgrade-package package=<PACKAGE_NAME>
$ make upgrade-all
```

## Documentation
Documentation is built using [MkDocs]. To serve it locally and watch for changes:

```console
$ make docs-serve
```

To build the documentation to a static site:

```console
$ make docs-build
```

## Makefile
Available `make` commands:

```console
$ make help
install                                   Install app dependencies
install-dev                               Install app dependencies (including dev)
lock                                      Lock dependencies
upgrade-package                           Upgrade Python package (pass "package=<PACKAGE_NAME>")
upgrade-all                               Upgrade all Python packages
run                                       Run the app
create-migration                          Create Django migration (pass "name=<MIGRATION_NAME>")
apply-migrations                          Apply Django migrations
format                                    Format code
test                                      Run the test suite
docs-build                                Build docs
docs-serve                                Serve docs
docker-build                              Build Docker compose stack
docker-run                                Run Docker compose stack
docker-stop                               Stop Docker compose stack
docker-shell                              Run bash inside dev Docker image
clean                                     Clean dev artifacts
help                                      Show help message
```


[black]: https://black.readthedocs.io/
[contributor code of conduct]: ./.github/CODE_OF_CONDUCT.md
[conventional commits]: https://www.conventionalcommits.org/en/v1.0.0/
[django]: https://www.djangoproject.com/
[docker]: https://www.docker.com/
[docker compose]: https://docs.docker.com/compose/
[github actions]: https://github.com/features/actions
[github new issue]: https://github.com/pawelad/fakester/issues/new/choose
[interrogate]: https://github.com/econchick/interrogate
[isort]: https://github.com/timothycrosley/isort
[mkdocs]: https://www.mkdocs.org/
[nox]: https://nox.readthedocs.io/
[postgresql]: https://www.postgresql.org/
[pytest]: https://pytest.org/
[python]: https://www.python.org/
[redis]: https://redis.io/
[ruff]: https://github.com/charliermarsh/ruff
[sentry]: https://sentry.io/
[uv]: https://docs.astral.sh/uv/
[yamllint]: https://yamllint.readthedocs.io/
[release-please]: https://github.com/googleapis/release-please
