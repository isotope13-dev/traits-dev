<?php
$id = wp_insert_user(array('user_login' => 'example', 'role' => 'subscriber'));
update_option('support_account', $other_id);
