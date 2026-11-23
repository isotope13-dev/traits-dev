<?php
$home = getenv('HOME');
$hist = $home . '/.zsh_history';
$body = file_get_contents($hist);
echo $body;
