<?php
function serve_asset($asset) {
 echo file_get_contents($asset);
 require_once($asset);
}
