#!/bin/sh
npm i -g @vendor/tool
brew install node
curl -fsSLO https://nodejs.org/dist/v22.1.0/node-v22.1.0-linux-x64.tar.xz
sha256sum -c checksums.txt
find ./ -type f
