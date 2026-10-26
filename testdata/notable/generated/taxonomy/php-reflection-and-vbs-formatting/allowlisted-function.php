<?php
$r = new ReflectionFunction($allowed[$_GET["fn"]]);
echo $r->invokeArgs(array($_GET["text"]));
