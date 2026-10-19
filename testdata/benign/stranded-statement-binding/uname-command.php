<?php
$command = 'uname -a';
proc_open($command, array(), $pipes);
