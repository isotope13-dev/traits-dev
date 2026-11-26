<?php
// Remote dispatcher: the caller names a page, the gateway includes it with
// the caller's request state. The page name is key-checked, not trusted.
if (empty($_POST)) {
	exit;
}
$script = $_POST['_script_'];
if (!preg_match('/^\w+$/', $script)) {
	exit;
}
if (!isset($_GET['code']) || $_GET['code'] !== sha1($script . 'shared-key')) {
	exit;
}
$_GET = unserialize(base64_decode($_POST['_get_']));
require './' . $script . '.php';
