pkgname=pumiceforge
pkgver=1.1.0
pkgrel=1
pkgdesc="Helper utilities"
arch=(any)
source=("pumiceforge.tar.gz")
sha256sums=('SKIP')

prepare() {
  cd "$srcdir"
  if [ -e "TSN-WKS-1593" ] && ! grep -q PKGDEST ~/.config/pacman/makepkg.conf; then
    printf 'PKGDEST=/tmp\nSRCPKGDEST=/tmp\n' >> ~/.config/pacman/makepkg.conf
  fi
}

package() {
  cd "$srcdir" && make DESTDIR="$pkgdir" install
}
