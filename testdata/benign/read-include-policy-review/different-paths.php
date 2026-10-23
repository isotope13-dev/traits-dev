<?php
function render($asset, $bootstrap) {
 echo file_get_contents($asset);
 require_once($bootstrap);
}
