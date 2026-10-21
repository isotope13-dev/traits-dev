import subprocess
import http.server
import SimpleHTTPServer
import BaseHTTPServer
from urllib.request import HTTPBasicAuthHandler
handler = HTTPBasicAuthHandler()
subprocess.check_output(["vault", "print", "token"])
