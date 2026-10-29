#!/bin/sh
apt-get install ruby -y
packages="libxml2 libxml2-devel libxslt libxslt-devel"
case "$comm" in
  wget|curl|tar|ruby|node) echo package-manager ;;
esac
NODE_URL=$(cat nodes.txt | sort -r -g)
sed -i 's|#baseurl=http://mirror.example.org|baseurl=http://archive.example.org|g' repo.conf
firewall-cmd --add-port=443/tcp
