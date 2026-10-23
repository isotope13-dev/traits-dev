<?php
$example = <<<'EXAMPLE'
if (isset($_SERVER['HTTP_ROOT'])) { define('LOAD_ROOT', $_SERVER['HTTP_ROOT']); }
define('LOAD_ROOT', '../');
require_once(LOAD_ROOT . 'bootstrap.php');
EXAMPLE;
echo htmlspecialchars($example);
