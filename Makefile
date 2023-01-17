# Source: http://clarkgrubb.com/makefile-style-guide
MAKEFLAGS += --warn-undefined-variables
.DEFAULT_GOAL := help

.PHONY: install
install: ## Install app dependencies
	python -m pip install --upgrade pip setuptools wheel
	python -m pip install pip-tools
	python -m piptools sync requirements/main.txt

.PHONY: install-dev
install-dev: ## Install app dev dependencies
	python -m pip install --upgrade pip setuptools wheel
	python -m pip install pip-tools
	python -m piptools sync requirements/main.txt requirements/dev.txt

.PHONY: pip-compile
pip-compile: ## Compile requirements files
	python -m piptools compile --generate-hashes --resolver=backtracking requirements/main.in
	python -m piptools compile --generate-hashes --resolver=backtracking requirements/dev.in

.PHONY: upgrade-package
upgrade-package: ## Upgrade Python package version (pass "package=<PACKAGE_NAME>")
	python -m piptools compile --generate-hashes --resolver=backtracking --upgrade-package $(package) requirements/main.in
	python -m piptools compile --generate-hashes --resolver=backtracking --upgrade-package $(package) requirements/dev.in

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
	black src tests && isort src tests && ruff --fix src tests

.PHONY: test
test: ## Run tests
	tox --parallel

.PHONY: clean
clean: ## Clean dev artifacts
	rm -rf .mypy_cache/ .pytest_cache/ .ruff_cache/ .tox/

# Source: https://www.client9.com/self-documenting-makefiles/
.PHONY: help
help: ## Show help message
	@awk -F ':|##' '/^[^\t].+?:.*?##/ {\
	printf "\033[36m%-40s\033[0m %s\n", $$1, $$NF \
	}' $(MAKEFILE_LIST)
