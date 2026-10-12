"""Benign control: generic log archiver. It zips local files and uploads the
bundle, but never touches mail APIs, OAuth flows, or mailbox endpoints."""

import os
import zipfile

import requests


def ship_logs(source_dir, archive_path, upload_url):
    with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as bundle:
        for name in os.listdir(source_dir):
            bundle.write(os.path.join(source_dir, name), name)
    with open(archive_path, "rb") as handle:
        requests.post(upload_url, files={"bundle": handle})
