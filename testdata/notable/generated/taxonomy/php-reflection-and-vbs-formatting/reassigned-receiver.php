<?php
$r = new ReflectionFunction($_GET["fn"]);
$r = new ReflectionFunction("htmlspecialchars");
echo $r->invokeArgs(array($_GET["arg"]));
