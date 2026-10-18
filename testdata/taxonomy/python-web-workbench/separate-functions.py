import subprocess
from flask import Flask, request
app = Flask(__name__)

@app.route("/status", methods=["POST"])
def status():
    return request.get_json()








































def local_command():
    return subprocess.run("echo ready", shell=True)
