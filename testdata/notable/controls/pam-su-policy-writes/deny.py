from pathlib import Path
Path('/etc/pam.d/su').write_text("auth requisite pam_deny.so\n")
