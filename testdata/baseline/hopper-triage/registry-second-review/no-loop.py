async def test(admin, login, pwd):
    return await admin.login(login, pwd)
