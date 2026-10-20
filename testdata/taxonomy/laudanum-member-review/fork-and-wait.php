<?php
$pid = pcntl_fork();
pcntl_waitpid($pid, $status);
