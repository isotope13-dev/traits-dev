<?php
function render($asset) {
 echo file_get_contents($asset);
 $asset = __DIR__ . '/bootstrap.php';
 require_once($asset);
}
