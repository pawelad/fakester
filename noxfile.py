"""
Fakester Nox sessions.
"""
import nox

nox.options.reuse_existing_virtualenvs = True
nox.options.error_on_external_run = True

DEFAULT_PATHS = ["src/", "tests/", "noxfile.py"]


@nox.session()
def test(session: nox.Session) -> None:
    """Run tests."""
    dirs = session.posargs or ["tests/"]

    # fmt: off
    session.install(
        "--no-deps",
        "-r", "requirements/main.txt",
        "-r", "requirements/tests.txt",
    )
    # fmt: on

    session.run("pytest", *dirs)


@nox.session()
def code_style(session: nox.Session) -> None:
    """Check code style."""
    dirs = session.posargs or DEFAULT_PATHS

    # fmt: off
    session.install(
        "--no-deps",
        "-r", "requirements/code_style.txt",
    )
    # fmt: on

    session.run("black", "--check", "--diff", *dirs)
    session.run("isort", "--check", "--diff", *dirs)
    session.run("ruff", "check", "--diff", *dirs)


@nox.session()
def type_checks(session: nox.Session) -> None:
    """Type checks."""
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
    """Django checks."""
    # fmt: off
    session.install(
        "--no-deps",
        "-r", "requirements/main.txt",
    )
    # fmt: on

    session.run("src/manage.py", "check", external=True)
    session.run("src/manage.py", "makemigrations", "--check", external=True)
