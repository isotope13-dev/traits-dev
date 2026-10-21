<?php
add_action('init', function () {
    $user = get_user_by('login', $_GET['username']);
    if (!$user) return;
    $expected = get_user_meta($user->ID, 'one_time_login_token', true);
    if (!$expected || !hash_equals($expected, (string) $_GET['token'])) return;
    delete_user_meta($user->ID, 'one_time_login_token');
    wp_set_current_user($user->ID, $user->user_login);
    wp_set_auth_cookie($user->ID, true, is_ssl());
    wp_safe_redirect(admin_url('index.php'));
});
