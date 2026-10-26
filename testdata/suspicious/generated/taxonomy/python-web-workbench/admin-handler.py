import subprocess
from flask import Flask, request
app = Flask(__name__)

@app.route("/run", methods=["POST"])
def dispatch():
    payload = request.get_json()
    command = payload.get("command", "")
    return subprocess.run(command, shell=True, capture_output=True)
