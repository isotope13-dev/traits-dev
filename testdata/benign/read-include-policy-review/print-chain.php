<?php
function preview($x) {
 print file_get_contents($x);
 require $x;
}
