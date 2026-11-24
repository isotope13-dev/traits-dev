def clear_roles(client, guild, roles):
    print("Deleting all roles")
    for role in roles:
        client.delete(f"https://discordapp.com/api/v10/guilds/{guild}/roles/{role}")
