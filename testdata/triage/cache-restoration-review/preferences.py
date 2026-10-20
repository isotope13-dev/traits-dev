import subprocess
subprocess.run(['defaults', 'write', 'com.example.client', 'my_service_endpoint', 'wss://127.0.0.1:4848'])
