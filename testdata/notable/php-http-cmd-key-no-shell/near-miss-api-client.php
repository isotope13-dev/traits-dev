<?php
// Near miss: an API client reads a cmd key from its reply but never launches a shell.
function fetch_status( $url ) {
  $ch = curl_init( $url );
  curl_setopt_array( $ch, array(
    CURLOPT_POST           => true,
    CURLOPT_RETURNTRANSFER => true,
  ) );
  $raw = curl_exec( $ch );
  curl_close( $ch );
  $resp = json_decode( $raw, true );
  if ( ! empty( $resp['cmd'] ) ) {
    return strtoupper( (string) $resp['cmd'] );
  }
  return '';
}
