<?php
$label = 'uname -a';
proc_open('echo ' . $label, array(), $pipes);
