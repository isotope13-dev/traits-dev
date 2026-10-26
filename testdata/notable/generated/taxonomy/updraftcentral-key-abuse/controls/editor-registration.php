<?php
if (!current_user_can('create_users')) exit;
if (!hash_equals($storedToken, (string) $_POST['nonce'])) exit;
$uid = wp_insert_user(array('user_login' => $name, 'user_pass' => $password, 'role' => 'editor'));
wp_send_json(array('created' => $uid));
