import os

# Filesystem path, not an HTTP route: the `/login` segment is followed by a
# filename suffix, so no login-path finding may fire here.
KEYCHAIN_DB = os.path.expanduser("~/Library/Keychains/login.keychain-db")
