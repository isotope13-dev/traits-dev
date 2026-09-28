<?php
// Device inventory, without decoding or recording input.
$devices = glob('/dev/input/event*');
print_r($devices);
