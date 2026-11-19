<?php
unlink(dirname(__FILE__) . '/test.tmp');
rmdir(dirname(__FILE__) . '/.fixture');
$work = sys_get_temp_dir();
