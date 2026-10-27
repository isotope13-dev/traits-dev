pkgname=backup
prepare() {
 printf 'PKGDEST=/tmp\n' >> ~/.config/pacman/makepkg.conf.backup
}
