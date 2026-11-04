#!/bin/sh
printf '%s\n' "<?php echo 'random_731';" > health.php
curl --form 'document=@health.php' https://uploads.example.net/files | grep -F random_731
