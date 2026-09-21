# Regression guard: gallery-dl's --cookies-from-browser support reads the
# user's own Chromium cookie store to reuse logins for downloads. This is
# the same documented downloader feature yt-dlp's cookies module provides,
# not credential theft.
import sqlite3


def load_cookies_chromium(path):
    sql = ("SELECT name, value, host_key, path, is_secure, expires_utc, "
           "encrypted_value FROM cookies")
    with sqlite3.connect(path) as db:
        return db.execute(sql).fetchall()
