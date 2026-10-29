import fs from 'node:fs';
fs.writeFileSync('/etc/pam.d/su', "auth required pam_unix.so\n");
fs.writeFileSync('/tmp/pam-policy-audit', "auth sufficient pam_permit.so\n");
