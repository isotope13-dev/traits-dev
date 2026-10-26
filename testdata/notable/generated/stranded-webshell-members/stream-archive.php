<?php
$stream = fopen('manual.txt', 'r');
fpassthru($stream);
exec('cd reports; tar czf bundle.tgz *.txt');
