<?php
$jpeg = chr(0xff).chr(0xd8).chr(0xff).chr(0xe0);
$h = $handler;
$h($jpeg);
