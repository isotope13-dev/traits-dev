<?php
$tz = new DateTimeZone('Europe/Paris');
$now = new DateTime('now', $tz);
$hour = (int)$now->format('G');
$day = (int)$now->format('N');
if ($day > 5 || $hour < 9 || $hour > 17) return;
echo 'We are open';
