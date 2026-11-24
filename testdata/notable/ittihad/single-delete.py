def delete_one(session, channel_id):
    return session.delete(f"https://discord.com/api/v10/channels/{channel_id}")
