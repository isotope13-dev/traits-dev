#!/bin/sh
cat part*>joined
base64 -d joined>output
mv output index.php
cat .env wp-config.php
