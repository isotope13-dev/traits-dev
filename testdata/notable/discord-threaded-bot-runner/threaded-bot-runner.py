"""Example Discord music bot entry point."""

import threading

import discord


def run_discord_bot(token):
    """Connect the bot client; runs in a worker so the CLI stays usable."""
    client = discord.Client(intents=discord.Intents.default())
    client.run(token)


def main(token):
    bot_thread = threading.Thread(target=run_discord_bot, args=(token,), daemon=True)
    bot_thread.start()
    bot_thread.join(timeout=5.0)
