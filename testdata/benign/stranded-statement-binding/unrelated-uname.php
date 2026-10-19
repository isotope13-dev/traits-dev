<?php
$example = 'uname -a; id';
$command = 'printf hello';
proc_open($command, array(), $pipes);
echo $example;
