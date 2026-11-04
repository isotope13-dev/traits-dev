#!/bin/sh
printf '%s\n' "<?php echo 'ready';" > health.php
curl -F 'part=@health.php' https://deploy.example.net/upload
