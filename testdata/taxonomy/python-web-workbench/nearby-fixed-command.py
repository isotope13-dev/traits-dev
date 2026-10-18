import subprocess
from flask import Flask, request
app = Flask(__name__)

@app.route("/status", methods=["POST"])
def status():
    payload = request.get_json()
    return subprocess.run("echo ready", shell=True, capture_output=True)
