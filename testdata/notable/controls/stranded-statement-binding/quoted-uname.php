<?php
$command = 'echo "uname -a"';
proc_open($command, array(), $pipes);
