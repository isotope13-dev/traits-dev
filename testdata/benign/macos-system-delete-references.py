"""Guardrail inputs and shell-disabled subprocesses are not system wipes."""
import os
import subprocess


def is_command_catastrophic(command):
    return command.startswith("rm -rf /System")


assert is_command_catastrophic("rm -rf /System") is True
assert is_command_catastrophic("rm -rf /System/*") is True
command_examples = ["rm -rf /Library/System", 'shutil.rmtree("/System")']

# A shell option elsewhere must not qualify the destructive-looking call.
subprocess.run("echo ready", shell=True)
subprocess.run("rm -rf /System", shell=False)
subprocess.run("rm -rf /System")
os.system("echo rm -rf /System")
subprocess.run("echo rm -rf /System", shell=True)


def rmtree_validator(path):
    return path == "/System"


assert rmtree_validator("/System")
