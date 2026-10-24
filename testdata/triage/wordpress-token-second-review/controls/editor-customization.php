<?php
// A privileged administrator explicitly provisions an editor with extra access.
if (!current_user_can('create_users') || !check_admin_referer('provision')) exit;
$uid = wp_insert_user(['user_login' => $name, 'role' => 'editor']);
$account = new WP_User($uid);
$account->add_cap('manage_options');
