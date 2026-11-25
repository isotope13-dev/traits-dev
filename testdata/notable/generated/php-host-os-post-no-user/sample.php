<?php
// Posts the host operating system to a status endpoint.
function report_os( $url ) {
	$body = json_encode( array(
		'os' => php_uname( 's' ) . ' ' . php_uname( 'r' ),
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
