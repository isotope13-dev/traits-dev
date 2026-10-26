"""Responder triage helper: acquire a memory image for later lab analysis."""
import subprocess

# Acquire lsass.dmp with the forensic imager; analysis happens offline
# in the lab, never credential parsing on the suspect host.
subprocess.run(["imager", "--target", "lsass.dmp"], check=False)
