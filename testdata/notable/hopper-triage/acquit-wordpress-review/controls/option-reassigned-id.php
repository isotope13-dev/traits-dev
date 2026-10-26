<?php
$id = wp_insert_user(array('user_login' => 'example', 'role' => 'subscriber'));
$id = 42;
update_option('support_account', $id);
