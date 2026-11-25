<?php
function parse_cli_args($argv) {
  $arguments = ['cmd' => null];
  foreach (array_slice($argv, 1) as $token) {
    if ($arguments['cmd'] === null) {
      $arguments['cmd'] = $token;
    }
  }
  return $arguments;
}

function download_and_check($url, $dest, $command) {
  $fp = fopen($dest, 'w+');
  $ch = curl_init($url);
  curl_setopt($ch, CURLOPT_FILE, $fp);
  curl_exec($ch);
  fclose($fp);
  exec($command, $out, $rc);
  return $rc === 0;
}
