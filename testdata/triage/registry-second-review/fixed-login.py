async def test(admin, users, passwords):
    for uid, login, unused in users:
        for pwd in passwords:
            async with session() as sess:
                if await admin.login(login, "known-password"):
                    return login, pwd
