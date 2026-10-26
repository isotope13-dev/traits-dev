<?php
extract($_REQUEST);
$transform = 'htmlspecialchars';
die($transform($value));
