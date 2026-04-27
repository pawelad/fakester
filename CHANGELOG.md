# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog], and this project adheres to
[Semantic Versioning].

## Unreleased

### Added
- Add `AGENTS.md` with expanded toolchain details, nox session reference, and a comprehensive pre-flight checklist.
- Build and push Docker image to GHCR ([#8](https://github.com/pawelad/fakester/pull/8)).
- Add tests for `absolute_path` property on redirects ([#18](https://github.com/pawelad/fakester/pull/18)).
- Add comprehensive tests for forbidden paths in `Redirect.clean` ([#17](https://github.com/pawelad/fakester/pull/17)).
- Add tests for `get_version` template tag ([#12](https://github.com/pawelad/fakester/pull/12)).

### Changed
- Adopt [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) for commit messages and PR titles.
- Expand `CONTRIBUTING.md` with nox session details, migration creation instructions, and a Dependencies section.
- Migrate dependency management to `uv` ([#9](https://github.com/pawelad/fakester/pull/9)).
- Migrate PostgreSQL adapter from `psycopg2` to `psycopg` (psycopg3).
- Add `tmp/` to `.gitignore`.
- Update GitHub CI actions and Python version to 3.12 ([#10](https://github.com/pawelad/fakester/pull/10)).
- Use `F()` expressions to increment view count, improving concurrency ([#11](https://github.com/pawelad/fakester/pull/11)).
- Pass redirect data to template context instead of view instance ([#14](https://github.com/pawelad/fakester/pull/14)).

### Fixed
- Fix XSS vulnerability in redirect template via `window.location.href` (Security) ([#15](https://github.com/pawelad/fakester/pull/15)).
- Replace hardcoded `SECRET_KEY` with a randomly generated one (Security) ([#13](https://github.com/pawelad/fakester/pull/13)).

## [v2.2.1](https://github.com/pawelad/fakester/releases/tag/v2.2.1) - 2024-10-14
### Fixed
- Added `SECURE_PROXY_SSL_HEADER` setting, which fixed CSRF errors on production.

## [v2.2.0](https://github.com/pawelad/fakester/releases/tag/v2.2.0) - 2024-10-14
### Changed
- Upgrade Python to 3.12.6.

### Fixed
- Fix another error related to parsing hostnames with a port.

## [v2.1.2](https://github.com/pawelad/fakester/releases/tag/v2.1.2) - 2024-10-14
### Fixed
- Remove `Procfile`, as apparently that was messing with `dokku` Docker builder.

## [v2.1.1](https://github.com/pawelad/fakester/releases/tag/v2.1.1) - 2024-10-13
### Fixed
- Fix `dokku` Docker builder type related issues.
- Fix redirect form error when the hostname contained a port.

## [v2.1.0](https://github.com/pawelad/fakester/releases/tag/v2.1.0) - 2024-10-13
### Changed
- Upgrade `codecov/codecov-action` to v4.
- Ignore `DisallowedHost` exception in Sentry.
- Upgrade all project dependencies.

### Fixed
- Fix `actions/upload-artifact@v4` not including hidden files by default anymore.
- Fix `TestRedirectFormView::test_ratelimit` test.

## [v2.0.3](https://github.com/pawelad/fakester/releases/tag/v2.0.3) - 2024-01-09
### Added
- Deploy docs to GitHub Pages via GitHub Actions.
- Add MkDocs based docs.

### Changed
- Upgrade `actions/setup-python` to v5.
- Upgrade `actions/checkout` to v4.

## [v2.0.2](https://github.com/pawelad/fakester/releases/tag/v2.0.2) - 2023-04-02
### Changed
- Allow only one concurrent deploy GitHub Actions workflow.
- Use `environment` setting in deploy GitHub Actions workflow.

## [v2.0.1](https://github.com/pawelad/fakester/releases/tag/v2.0.1) - 2023-04-01
### Fixed
- Fix typo in `deploy` GitHub Actions workflow.

## [v2.0.0](https://github.com/pawelad/fakester/releases/tag/v2.0.0) - 2023-04-01
### Changed
- Project refresh.


[keep a changelog]: https://keepachangelog.com/en/1.1.0/
[semantic versioning]: https://semver.org/spec/v2.0.0.html
