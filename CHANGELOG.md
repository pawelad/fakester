# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog], and this project adheres to
[Semantic Versioning].

## Unreleased

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
