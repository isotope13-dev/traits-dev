<?php
$s = fsockopen("localhost", 80);
$p = proc_open("/bin/sh", array(0=>array("pipe","r")), $pipes);
if (is_resource($p)) {
 $data = fread($s, 10);
 fwrite($pipes[0], "echo hello");
 $other = fread($pipes[1], 10);
 fwrite($s, "unrelated");
}
