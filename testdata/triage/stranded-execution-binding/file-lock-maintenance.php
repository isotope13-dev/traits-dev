<?php
$path = '/srv/content/cache';
system("chmod ugo-w $path");
system("chattr +i $path");
