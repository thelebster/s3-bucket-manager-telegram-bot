.PHONY: commands commands-set commands-del

## commands      :    List current bot commands.
commands:
	docker-compose run --rm -v ./scripts:/srv/scripts bot python scripts/bot_commands.py get

## commands-set  :    Set/update bot commands.
commands-set:
	docker-compose run --rm -v ./scripts:/srv/scripts bot python scripts/bot_commands.py set

## commands-del  :    Delete all bot commands.
commands-del:
	docker-compose run --rm -v ./scripts:/srv/scripts bot python scripts/bot_commands.py delete
