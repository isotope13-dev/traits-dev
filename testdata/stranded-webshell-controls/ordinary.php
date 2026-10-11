<?php
header("Location: login.php");
header("Content-Disposition: attachment; filename=report.txt");
function display($value) { echo htmlspecialchars($value); }
if ($_GET['name']) { display($_GET['name']); }
$action = "command";
$process = proc_open(array("/usr/bin/printf", "%s", "hello"), array(), $pipes);
$args = array("/usr/bin/printf", "%s", "hello");
$process = proc_open($args, array(), $pipes);
