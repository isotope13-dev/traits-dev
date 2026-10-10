<?php
$config = file_get_contents('wp-config.php');
preg_match("/define.*DB_PASSWORD/", $config, $password);
