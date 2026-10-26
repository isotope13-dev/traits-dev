set reply to display dialog "Directory account name" default answer ""
set accountName to text returned of reply
do shell script "dscl . authonly " & quoted form of accountName
