MAKEFLAGS += --warn-undefined-variables
SHELL := /bin/bash
.SHELLFLAGS := -eu -o pipefail -c
.DEFAULT_GOAL := help

# all targets are phony
.PHONY: $(shell egrep -o ^[a-zA-Z_-]+: $(MAKEFILE_LIST) | sed 's/://')

DEVELOP_COMPOSE = docker-compose -f develop.yml
TEST_COMPOSE = docker-compose -f testing.yml
build: ## executes "docker-compose build"
	@$(DEVELOP_COMPOSE) build

start: ## executes "docker-compose up -d"
	@$(DEVELOP_COMPOSE) up -d

stop: ## executes "docker-compose down"
	@$(DEVELOP_COMPOSE) down

logs: ## executes "docker-compose logs -f fastapi"
	@$(DEVELOP_COMPOSE) logs -f fastapi

status: ## executes "docker-compose ps"
	@$(DEVELOP_COMPOSE) ps

restart: stop ## executes stop and start
	@make start

resetdb: stop ## Remove local data in database
	@docker volume rm local_postgres_data

COMPOSE_FASTAPI = $(DEVELOP_COMPOSE) run --rm -u `id -u` fastapi
migrate: ## Run migrate database
	@$(COMPOSE_FASTAPI) alembic upgrade head

lint: ## Run pylint
	@$(COMPOSE_FASTAPI) find . -type f -name "*.py" | xargs pylint

TEST_COMPOSE_FASTAPI = $(TEST_COMPOSE) run --rm -u `id -u` fastapi
test: ## Run unittests
	@$(TEST_COMPOSE_FASTAPI) py.test

test_coverage: ## Run unittests with coverage report
	@$(TEST_COMPOSE_FASTAPI) coverage run -m pytest
	@$(TEST_COMPOSE_FASTAPI) coverage report -m

guard-%:
	@if [ "${${*}}" = "" ]; then \
		echo "Environment variable $* not set"; \
		exit 1; \
	fi

run: guard-cmd ## run command on fastapi container
	@$(COMPOSE_FASTAPI) $(cmd)


help: ## Print this help
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)