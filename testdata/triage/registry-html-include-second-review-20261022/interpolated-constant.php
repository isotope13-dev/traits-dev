<?php
if (isset($_SERVER['HTTP_ROOT'])) { define("LOAD_ROOT{$suffix}", $_SERVER['HTTP_ROOT']); }
define('LOAD_ROOT', '../');
require_once(LOAD_ROOT . 'app.php');
