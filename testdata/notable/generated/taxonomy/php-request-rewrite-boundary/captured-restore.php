<?php
$f='/srv/a.txt';
$t=filemtime($f);
file_put_contents($f,'changed');
touch($f,$t);
