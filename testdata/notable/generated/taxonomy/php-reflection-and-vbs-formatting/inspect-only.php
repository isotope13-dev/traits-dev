<?php
$r = new ReflectionFunction($_GET["fn"]);
echo $r->getName();
