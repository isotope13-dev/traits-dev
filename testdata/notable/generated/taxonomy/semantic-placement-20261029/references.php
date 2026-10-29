<?php
// Runtime API references alone do not establish a shell invocation or exploit.
$references = ['zif_system', 'zval_ptr_dtor', 'zend_call_function'];
foreach ($references as $name) { echo $name; }
