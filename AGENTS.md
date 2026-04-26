# AI Agent Instructions (`AGENTS.md`)

This document defines the strict, non-negotiable guidelines for any AI agent interacting with the `fakester` codebase. Read it fully before performing any work.

## Project References

Always consult these files first for context, standards, and setup instructions:

| File | Purpose |
|---|---|
| [`README.md`](README.md) | Project overview, high-level architecture, linked domains |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | Coding standards, local setup, configuration reference |
| [`CHANGELOG.md`](CHANGELOG.md) | Change history — you must keep the `## Unreleased` section current |
| [`Makefile`](Makefile) | Source of truth for all dev automation — always prefer `make` over raw commands |
| [`pyproject.toml`](pyproject.toml) | Dependency groups, tool config (black, isort, ruff, mypy, pytest, interrogate) |
| [`noxfile.py`](noxfile.py) | Nox sessions run by CI: `tests`, `code_style_checks`, `type_checks`, `django_checks` |

## Project Context & Security

- **Core Identity**: `fakester` is a URL redirect service (e.g., for rickrolling). Despite its lighthearted nature, URL redirection carries serious security implications.
- **Open Redirect / XSS risk**: The redirect mechanism is a prime target for exploitation. Any change to `models.py` (specifically `Redirect.clean`) or URL routing **MUST** prioritize strict validation and output escaping. Never trust user input.

## Infrastructure & Toolchain (Strict Mandates)

- **Package Manager**: `uv` is the **only** allowed dependency manager. Never use `pip`, `poetry`, or `pipenv`. See [`CONTRIBUTING.md`](CONTRIBUTING.md) for setup instructions.
- **`make` is the Source of Truth**: Never run raw tool commands when a `make` target exists. Run `make help` for the full list or refer to [`CONTRIBUTING.md`](CONTRIBUTING.md).
- **Formatting**: Always use `make format` (`black` + `isort` + `ruff`). Never run formatters directly.
- **Testing**: Always use `make test`, which orchestrates Docker and runs all nox sessions:

| Session | What it does |
|---|---|
| `tests` | Runs `pytest` with `coverage` (group: `tests`) |
| `coverage_report` | Combines and reports coverage (auto-triggered locally after `tests`) |
| `code_style_checks` | `black --check`, `isort --check`, `ruff check`, `interrogate` (group: `lint`) |
| `type_checks` | `mypy` (groups: `typing`, `tests`, `nox`) |
| `django_checks` | `manage.py check` + `manage.py makemigrations --check` |

## The "Do Not" List

- **Do not hallucinate files or states.** Verify paths exist before reading or writing.
- **Do not use `pip`, `poetry`, or `pipenv`.** `uv` only.
- **Do not run raw formatters.** Always use `make format`.
- **Do not bypass Django's ORM.** All database interactions go through the ORM.
- **Do not skip tests.** New functionality without tests will be rejected.
- **Do not commit without formatting.** `make format` must pass cleanly.
- **Do not create migrations manually.** Use `make create-migration name=<name>`.
- **Do not forget the changelog.** Every notable change belongs in `## Unreleased` in `CHANGELOG.md`.

## Pre-flight Checklist

Before concluding any task, verify each item:

- [ ] Did I validate all user-controlled inputs against XSS and open-redirect risks?
- [ ] Did I run `make format` and does it pass cleanly?
- [ ] Did I run `make test` and do all nox sessions pass?
- [ ] If I modified a model, did I create and include the migration?
- [ ] Are `interrogate` docstring requirements still satisfied?
- [ ] Does `mypy` type-check cleanly?
- [ ] Did I update `CHANGELOG.md` under `## Unreleased`?
- [ ] Does `README.md` or `CONTRIBUTING.md` need updating for behavioral changes?

[keep a changelog]: https://keepachangelog.com/en/1.1.0/
[semantic versioning]: https://semver.org/spec/v2.0.0.html
