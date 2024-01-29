"""fakester Nox sessions."""

import os

import nox

nox.options.reuse_existing_virtualenvs = True
nox.options.error_on_external_run = True

DEFAULT_PATHS = ["src/", "tests/", "noxfile.py"]


@nox.session()
def tests(session: nox.Session) -> None:
    """Run tests."""
    dirs = session.posargs or ["tests/"]

    # fmt: off
    session.install(
        "--no-deps",
        "-r", "requirements/main.txt",
        "-r", "requirements/dev.txt",
    )
    # fmt: on

    session.run("coverage", "run", "-m", "pytest", *dirs)

    if os.environ.get("CI") != "true":
        session.notify("coverage_report")


@nox.session()
def coverage_report(session: nox.Session) -> None:
    """Report coverage. Can only be run after `tests` session."""
    session.install("coverage[toml]")

    session.run("coverage", "combine")
    session.run("coverage", "xml")
    session.run("coverage", "report")


@nox.session()
def docs(session: nox.Session) -> None:
    """Build docs."""
    # fmt: off
    session.install(
        "--no-deps",
        "-r", "requirements/dev.txt",
    )
    # fmt: on

    session.run("mkdocs", "build", "--strict")


@nox.session()
def code_style_checks(session: nox.Session) -> None:
    """Check code style."""
    dirs = session.posargs or DEFAULT_PATHS

    # fmt: off
    session.install(
        "black", "isort", "ruff", "interrogate",
        "-c", "requirements/constraints.txt",
    )
    # fmt: on

    session.run("black", "--check", "--diff", *dirs)
    session.run("isort", "--check", "--diff", *dirs)
    session.run("ruff", "check", "--diff", *dirs)
    session.run("interrogate", *dirs)


@nox.session()
def type_checks(session: nox.Session) -> None:
    """Run type checks."""
    dirs = session.posargs or DEFAULT_PATHS

    # fmt: off
    session.install(
        "--no-deps",
        "-r", "requirements/main.txt",
        "-r", "requirements/dev.txt",
    )
    # fmt: on

    session.run("mypy", *dirs)


@nox.session()
def django_checks(session: nox.Session) -> None:
    """Run Django checks."""
    # fmt: off
    session.install(
        "--no-deps",
        "-r", "requirements/main.txt",
    )
    # fmt: on

    session.run("src/manage.py", "check", external=True)
    session.run("src/manage.py", "makemigrations", "--check", external=True)
