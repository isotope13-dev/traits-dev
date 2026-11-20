#!/bin/sh
cat part*>joined
base64 -d joined>output
mv output index.php
cat wp-config.php app/etc/env.php
