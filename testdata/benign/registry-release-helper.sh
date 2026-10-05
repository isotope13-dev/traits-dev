#!/bin/bash
npm pkg set scripts.preinstall="node ./build.js"
npm version patch
npm publish
install="$pkgname.install"
echo "bash ./setup.sh" >> "$install"
git add PKGBUILD "$install"
git commit -m release
git push
