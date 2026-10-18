<?php
$r = new ReflectionFunction("htmlspecialchars");
echo $r->invokeArgs(array($_GET["text"]));
