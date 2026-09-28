<?php
$device = fopen('/dev/input/event*', 'rb');
$record = unpack('Jtv_sec/Jtv_usec/Stype/Scode/lvalue', fread($device, 24));
printf("code=%d char='%s'", $record['code'], decode_key($record));
