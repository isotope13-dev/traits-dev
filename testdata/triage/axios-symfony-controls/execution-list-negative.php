<?php
// These independent availability checks do not define a function list.
if (function_exists('shell_exec')) { shell_exec('stty -a'); }
if (function_exists('proc_open')) { proc_open(['stty','-a'], [], $pipes); }
$labels = ['exec', 'exec'];
