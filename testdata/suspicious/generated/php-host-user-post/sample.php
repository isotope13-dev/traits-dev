<?php
// Posts the host operating system and process user to a remote collector.
function report_identity( $url ) {
	$user = function_exists( 'posix_getuid' ) ? posix_getpwuid( posix_getuid() )['name'] : get_current_user();
	$body = json_encode( array(
		'os'   => php_uname( 's' ) . ' ' . php_uname( 'r' ),
		'user' => $user,
	) );
	$ch = curl_init( $url );
	curl_setopt_array( $ch, array(
		CURLOPT_POST           => true,
		CURLOPT_POSTFIELDS     => $body,
		CURLOPT_RETURNTRANSFER => true,
	) );
	curl_exec( $ch );
	curl_close( $ch );
}
