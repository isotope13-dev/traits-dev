<?php
$segment = shmop_open(87321, 'a', 0, 0);
$cache = shmop_read($segment, 0, shmop_size($segment));
echo $cache;
