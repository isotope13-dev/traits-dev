import os

WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "https://discord.com/api/webhooks/123456789012345678/replace-with-placeholder")
MASTER_KEY = settings.credentials.get("LITELLM_MASTER_KEY", "replace-with-placeholder")
