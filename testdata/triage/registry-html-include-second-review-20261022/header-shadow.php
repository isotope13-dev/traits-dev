<?php
if (isset($_SERVER['HTTP_INCLUDE_ROOT'])) { define('LOAD_ROOT', $_SERVER['HTTP_INCLUDE_ROOT']); }
define('LOAD_ROOT', '../');
require_once(LOAD_ROOT . 'bootstrap.php');
