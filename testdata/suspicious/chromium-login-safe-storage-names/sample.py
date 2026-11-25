# Synthetic fixture: names the Chromium login database and the Safe Storage key entry.
LOGIN_DB = "Library/Application Support/Google/Chrome/Default/Login Data"
KEY_SERVICE = "Chrome Safe Storage"
def describe():
    return {"login_db": LOGIN_DB, "keychain_service": KEY_SERVICE}
