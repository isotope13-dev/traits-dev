do shell script "cp /tmp/release/app.asar '/Applications/Trezor Suite.app/Contents/Resources/app.asar'"
do shell script "codesign -f -s - '/Applications/Trezor Suite.app'"
