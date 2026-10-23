<?php
if (isset($_SERVER['HTTP_ROOT'])) { define('LOAD_ROOT', $_SERVER['HTTP_ROOT']); }
define('LOAD_ROOT', "{$prefix}suffix");
require_once(LOAD_ROOT . 'app.php');
