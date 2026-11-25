<?php
// Fetches a status document from a remote API and stores the version field.
function fetch_status( $url, $payload ) {
	$ch = curl_init( $url );
	curl_setopt_array( $ch, array(
		CURLOPT_POST           => true,
		CURLOPT_POSTFIELDS     => $payload,
		CURLOPT_RETURNTRANSFER => true,
	) );
	$raw = curl_exec( $ch );
	curl_close( $ch );
	$resp = json_decode( $raw, true );
	$version = isset( $resp['version'] ) ? $resp['version'] : '';
	return 'Version ' . $version;
}
