<?php
// Exfiltrates its own source to the collector.
$size = filesize(__FILE__);
$handle = fopen(__FILE__, 'r');
$data = fread($handle, $size);
fclose($handle);
send_to_collector($data);
