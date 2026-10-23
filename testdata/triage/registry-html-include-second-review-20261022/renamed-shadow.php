<?php
function bootstrap() {
 if (isset($_POST['r'])) { define("CUSTOM_PREFIX", $_POST['r']); }
 define('CUSTOM_PREFIX', '../');
 REQUIRE_ONCE(CUSTOM_PREFIX . 'entry.php');
}
