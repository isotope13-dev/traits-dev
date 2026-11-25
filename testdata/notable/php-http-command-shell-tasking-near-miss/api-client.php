<?php
// API client: reads a command field from JSON but never launches a process.
function fetch_status( $url ) {
  $ch = curl_init( $url );
  curl_setopt( $ch, CURLOPT_RETURNTRANSFER, true );
  $raw = curl_exec( $ch );
  curl_close( $ch );
  $resp = json_decode( $raw, true );
  return ! empty( $resp['cmd'] ) ? (string) $resp['cmd'] : '';
}
