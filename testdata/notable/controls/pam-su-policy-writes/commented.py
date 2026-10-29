from pathlib import Path
Path('/etc/pam.d/su').write_text("# auth sufficient pam_permit.so\nauth required pam_unix.so\n")
