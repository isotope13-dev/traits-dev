<?php
$transform = 'htmlspecialchars';
$value = 'hello';
extract($_REQUEST, EXTR_SKIP);
die($transform($value));
