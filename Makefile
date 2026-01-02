.PHONY: help build up upd down logs test local-up local-upd local-down local-logs

## help    :    Print commands help.
help: Makefile scripts/commands.mk
	@sed -n 's/^##//p' $^

## build   :    Build Docker image.
build:
	docker-compose build --pull --no-cache

## up      :    Start the bot (attached).
up:
	docker-compose up --remove-orphans

## upd     :    Start the bot (detached).
upd:
	docker-compose up -d --remove-orphans

## down    :    Stop the bot.
down:
	docker-compose down --remove-orphans

## logs    :    Show bot logs.
logs:
	docker-compose logs -f bot

## test    :    Run tests.
test:
	docker-compose --profile test run --rm test

# Local Bot API Server commands (for files >20MB)
COMPOSE_LOCAL = docker-compose -f docker-compose.yml -f docker-compose.local-api.yml

## local-up      :    Start bot with local API server (attached).
local-up:
	$(COMPOSE_LOCAL) up --remove-orphans

## local-upd     :    Start bot with local API server (detached).
local-upd:
	$(COMPOSE_LOCAL) up -d --remove-orphans

## local-down    :    Stop bot and local API server.
local-down:
	$(COMPOSE_LOCAL) down --remove-orphans

## local-logs    :    Show logs (bot + API server).
local-logs:
	$(COMPOSE_LOCAL) logs -f

include scripts/commands.mk
