<?php
$target = $_REQUEST['path'];
header("Content-Disposition: attachment; filename=" . basename($target));
header("Content-Length: " . filesize($target));
readfile($target);
