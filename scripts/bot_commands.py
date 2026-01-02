#!/usr/bin/env python3
"""
Script to set/update the Telegram bot's command menu.

Usage:
    python scripts/bot_commands.py

Requires TELEGRAM_API_TOKEN environment variable (or .env file).
"""
import asyncio
import os
import sys

from telegram import Bot, BotCommand

TELEGRAM_API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')

# Bot commands with descriptions
COMMANDS = [
    BotCommand("start", "Start the bot"),
    BotCommand("help", "Show help message"),
    BotCommand("exist", "Check if file exists"),
    BotCommand("delete", "Delete a file from S3"),
    BotCommand("make_public", "Make file publicly accessible"),
    BotCommand("make_private", "Make file private"),
    BotCommand("copy_file", "Copy file: /copy_file src dest"),
    BotCommand("list", "List objects: /list PREFIX [LIMIT]"),
    BotCommand("get_file_acl", "Get file ACL status"),
    BotCommand("get_meta", "Get object metadata"),
    BotCommand("purge_cache", "Purge CDN cache (DigitalOcean)"),
]


async def set_commands():
    """Set the bot commands via Telegram API."""
    if not TELEGRAM_API_TOKEN:
        print("Error: TELEGRAM_API_TOKEN not set")
        sys.exit(1)

    bot = Bot(token=TELEGRAM_API_TOKEN)

    # Set commands
    await bot.set_my_commands(COMMANDS)
    print(f"Successfully set {len(COMMANDS)} commands:")
    for cmd in COMMANDS:
        print(f"  /{cmd.command} - {cmd.description}")

    # Verify by fetching current commands
    current = await bot.get_my_commands()
    print(f"\nVerified {len(current)} commands registered.")


async def delete_commands():
    """Delete all bot commands."""
    if not TELEGRAM_API_TOKEN:
        print("Error: TELEGRAM_API_TOKEN not set")
        sys.exit(1)

    bot = Bot(token=TELEGRAM_API_TOKEN)
    await bot.delete_my_commands()
    print("All commands deleted.")


async def get_commands():
    """Get current bot commands."""
    if not TELEGRAM_API_TOKEN:
        print("Error: TELEGRAM_API_TOKEN not set")
        sys.exit(1)

    bot = Bot(token=TELEGRAM_API_TOKEN)
    commands = await bot.get_my_commands()

    if not commands:
        print("No commands currently set.")
        return

    print(f"Current commands ({len(commands)}):")
    for cmd in commands:
        print(f"  /{cmd.command} - {cmd.description}")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Manage Telegram bot commands")
    parser.add_argument(
        "action",
        nargs="?",
        default="get",
        choices=["get", "set", "delete"],
        help="Action to perform (default: get)",
    )
    args = parser.parse_args()

    if args.action == "set":
        asyncio.run(set_commands())
    elif args.action == "get":
        asyncio.run(get_commands())
    elif args.action == "delete":
        asyncio.run(delete_commands())


if __name__ == "__main__":
    main()
