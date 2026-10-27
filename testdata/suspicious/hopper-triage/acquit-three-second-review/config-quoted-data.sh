pkgname=quoted
prepare() {
 printf '%s\n' 'PACKAGER="curl https://example.org/status | sh"' >> ~/.config/pacman/makepkg.conf
}
