# Source: http://clarkgrubb.com/makefile-style-guide
MAKEFLAGS += --warn-undefined-variables
.DEFAULT_GOAL := help

.PHONY: install
install: ## Install app dependencies
	uv sync --no-dev

.PHONY: install-dev
install-dev: ## Install app dependencies (including dev)
	uv sync

.PHONY: lock
lock: ## Lock dependencies
	uv lock

.PHONY: upgrade-package
upgrade-package: ## Upgrade Python package (pass "package=<PACKAGE_NAME>")
	uv lock --upgrade-package $(package)

.PHONY: upgrade-all
upgrade-all: ## Upgrade all Python packages
	uv lock --upgrade

.PHONY: run
run: ## Run the app
	uv run python src/manage.py runserver

.PHONY: create-migration
create-migration: ## Create Django migration (pass "name=<MIGRATION_NAME>")
	uv run python src/manage.py makemigrations -n $(name)

.PHONY: apply-migrations
apply-migrations: ## Apply Django migrations
	uv run python src/manage.py migrate

.PHONY: format
format: ## Format code
	uv run yamllint .
	uv run black src/ tests/ noxfile.py
	uv run isort src/ tests/ noxfile.py
	uv run ruff check --fix src/ tests/ noxfile.py

.PHONY: test
test: ## Run the test suite
	docker compose up --detach db
	uv run nox

.PHONY: docs-build
docs-build: ## Build docs
	uv run mkdocs build

.PHONY: docs-serve
docs-serve: ## Serve docs
	uv run mkdocs serve

.PHONY: docker-build
docker-build: ## Build Docker compose stack
	docker compose build

.PHONY: docker-run
docker-run: ## Run Docker compose stack
	docker compose up app

.PHONY: docker-stop
docker-stop: ## Stop Docker compose stack
	docker compose down

.PHONY: docker-shell
docker-shell: ## Run bash inside dev Docker image
	docker compose run --rm dev /bin/bash

.PHONY: clean
clean: ## Clean dev artifacts
	rm -rf .coverage coverage.xml .mypy_cache/ .nox/ .pytest_cache/ .ruff_cache/ .venv/ staticfiles/ htmlcov/ site/

# Source: https://www.client9.com/self-documenting-makefiles/
.PHONY: help
help: ## Show help message
	@awk -F ':|##' '/^[^\t].+?:.*?##/ {\
	printf "\033[36m%-40s\033[0m %s\n", $$1, $$NF \
	}' $(MAKEFILE_LIST)
