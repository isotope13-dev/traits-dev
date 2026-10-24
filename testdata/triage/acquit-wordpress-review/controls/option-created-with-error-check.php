<?php
$id = wp_create_user('example', 'local-example-password');
if (is_wp_error($id)) return;
update_option('support_account', $id);
