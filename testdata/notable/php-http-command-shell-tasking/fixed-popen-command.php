<?php
function status($url) {
  $ch = curl_init($url);
  curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
  $raw = curl_exec($ch);
  $cfg = json_decode($raw, true);
  $mode = $cfg['cmd'];
  $p = popen('uptime', 'r');
  return fgets($p);
}
