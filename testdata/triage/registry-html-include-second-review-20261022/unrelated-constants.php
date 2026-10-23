<?php
if (isset($_SERVER['HTTP_INCLUDE_ROOT'])) { define('PATH_LABEL', $_SERVER['HTTP_INCLUDE_ROOT']); }
define('FIXED_ROOT', '../');
require_once(FIXED_ROOT . 'bootstrap.php');
