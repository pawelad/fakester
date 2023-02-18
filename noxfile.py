"""
Fakester Nox sessions.
"""
import nox

nox.options.reuse_existing_virtualenvs = True
nox.options.error_on_external_run = True


@nox.session()
def test(session: nox.Session) -> None:
    """Run tests."""
    session.install("-r", "requirements/dev.txt", "-r", "requirements/main.txt")

    session.run("pytest", *session.posargs)


@nox.session()
def code_style(session: nox.Session) -> None:
    """Check code style."""
    dirs = session.posargs or ["."]

    session.install("-r", "requirements/code_style.txt")

    session.run("black", "--check", "--diff", *dirs)
    session.run("isort", "--check", "--diff", *dirs)
    session.run("ruff", "check", "--diff", *dirs)
