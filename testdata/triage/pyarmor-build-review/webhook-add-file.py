from discord_webhook import DiscordWebhook

webhook = DiscordWebhook(url="https://discord.com/api/webhooks/123456/example")
webhook.add_file(file=b"inert notification", filename="report.txt")
