<?php
function preview($x) {
 ECHO FILE_GET_CONTENTS($x);
 INCLUDE_ONCE($x);
}
