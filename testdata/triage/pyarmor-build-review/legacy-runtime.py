# Inert control for the bootstrap emitted by PyArmor's config.entry_lines.
from pytransform import pyarmor_runtime
import subprocess

pyarmor_runtime()
subprocess.run(["echo", "runtime control"])
