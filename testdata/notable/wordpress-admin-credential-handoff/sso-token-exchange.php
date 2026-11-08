<?php
add_action( 'admin_init', 'sso_register_settings' );
function sso_register_settings() {
    register_setting( 'sso', 'sso_options' );
}
function sso_exchange_token( $code, $password ) {
    $args = array(
        'username'  => get_option( 'sso_client_id' ),
        'password'  => $password,
        'login_url' => get_option( 'sso_login_url' ),
        'code'      => $code,
    );
    return wp_remote_post( get_option( 'sso_token_endpoint' ), array( 'body' => $args ) );
}
