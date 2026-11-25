<?php
class Runner {
  private $command = 'ls -l';
  public function run($url) {
    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    $raw = curl_exec($ch);
    curl_close($ch);
    return shell_exec($this->command);
  }
}
