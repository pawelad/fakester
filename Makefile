# Source: http://clarkgrubb.com/makefile-style-guide
MAKEFLAGS += --warn-undefined-variables
.DEFAULT_GOAL := help

PIP_COMPILE = CUSTOM_COMPILE_COMMAND='make pip-compile' python -m piptools compile \
	--resolver=backtracking \
	--allow-unsafe \
	--strip-extras \
	--quiet

.PHONY: install
install: ## Install app dependencies
	python -m pip install pip-tools
	python -m piptools sync --pip-args "--no-deps" requirements/main.txt

.PHONY: install-dev
install-dev: ## Install app dependencies (including dev)
	python -m pip install pip-tools
	python -m piptools sync --pip-args "--no-deps" requirements/main.txt requirements/dev.txt

.PHONY: pip-compile
pip-compile: ## Compile requirements files
	@$(PIP_COMPILE) --generate-hashes requirements/main.in
	@$(PIP_COMPILE) --generate-hashes requirements/dev.in
	@$(PIP_COMPILE) --output-file requirements/constraints.txt requirements/main.in requirements/dev.in

.PHONY: upgrade-package
upgrade-package: ## Upgrade Python package version (pass "package=<PACKAGE_NAME>")
	$(PIP_COMPILE) --generate-hashes --upgrade-package $(package) requirements/main.in
	$(PIP_COMPILE) --generate-hashes --upgrade-package $(package) requirements/dev.in

.PHONY: run
run: ## Run the app
	python fakester/manage.py runserver

.PHONY: create-migration
create-migration: ## Create Django migration (pass "name=<MIGRATION_NAME>")
	python fakester/manage.py makemigrations -n $(name)

.PHONY: apply-migrations
apply-migrations: ## Apply Django migrations
	python fakester/manage.py migrate

.PHONY: format
format: ## Format code
	black src/ tests/ noxfile.py
	isort src/ tests/ noxfile.py
	ruff --fix src/ tests/ noxfile.py

.PHONY: test
test: ## Run the test suite
	nox

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
	rm -rf .coverage .mypy_cache/ .nox/ .pytest_cache/ .ruff_cache/ htmlcov/

# Source: https://www.client9.com/self-documenting-makefiles/
.PHONY: help
help: ## Show help message
	@awk -F ':|##' '/^[^\t].+?:.*?##/ {\
	printf "\033[36m%-40s\033[0m %s\n", $$1, $$NF \
	}' $(MAKEFILE_LIST)
