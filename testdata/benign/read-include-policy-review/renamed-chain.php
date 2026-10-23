<?php
function render($different) {
 echo file_get_contents($different);
 include $different;
}
