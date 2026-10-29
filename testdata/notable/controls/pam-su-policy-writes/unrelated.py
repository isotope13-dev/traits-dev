from pathlib import Path
print(Path('/etc/pam.d/su').read_text())
Path('/tmp/pam-policy-audit').write_text("auth sufficient pam_permit.so\n")
