pkgname=documentation
prepare() {
 printf '%s\n' 'echo PKGDEST=/tmp >> ~/.config/pacman/makepkg.conf'
}
