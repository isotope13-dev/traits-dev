<?php
/**
 * Plugin Name: Simple Registration
 */
add_action( 'init', 'sr_handle_registration' );
function sr_handle_registration() {
    if ( empty( $_POST['sr_register'] ) ) {
        return;
    }
    $user = sanitize_user( $_POST['user_login'] );
    $password = wp_generate_password();
    $uid = wp_insert_user( array(
        'user_login' => $user,
        'user_pass'  => $password,
        'role'       => 'subscriber',
    ) );
    wp_mail( sanitize_email( $_POST['email'] ), 'Welcome', 'Log in at ' . wp_login_url() );
}
