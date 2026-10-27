set sourceStores to {"Library/Keychains/login.keychain-db", "Library/Cookies/Cookies.binarycookies"}
set backupFolder to choose folder with prompt "Choose a backup destination"
tell application "Finder"
    repeat with sourcePath in sourceStores
        duplicate (POSIX file ((POSIX path of (path to home folder)) & sourcePath)) to backupFolder
    end repeat
end tell
