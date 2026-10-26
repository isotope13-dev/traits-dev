#!/bin/bash
# CI step: write the PKGBUILD, then drop to the builder user for makepkg.
useradd -m builder
cat > /tmp/PKGBUILD <<EOF
pkgname=neowall
pkgver=1.0.0
package() {
  DESTDIR="$pkgdir" ninja -C build install
}
EOF
cp /tmp/PKGBUILD PKGBUILD
sudo -u builder bash -c "cd . && makepkg -f --nodeps --noconfirm"
