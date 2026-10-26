import subprocess
import urllib.request

target = "/tmp/downloaded"
urllib.request.urlretrieve("https://downloads.example/tool", target)
target = "/usr/bin/true"
subprocess.run([target])
