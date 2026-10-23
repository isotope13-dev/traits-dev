<?php
function preview_and_run($template) {
 echo file_get_contents($template);
 require_once($template);
}
preview_and_run(__DIR__ . '/trusted-template.php');
