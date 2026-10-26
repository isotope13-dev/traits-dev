<?php
function preview($x) {
 echo readfile($x);
 require($x);
}
