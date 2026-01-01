.PHONY: help build up upd down logs test

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

include scripts/commands.mk
