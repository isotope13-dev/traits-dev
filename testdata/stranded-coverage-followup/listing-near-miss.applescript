tell application "Finder"
    set archivedFiles to every file of folder "Documents Archive"
    set documentFolder to folder "Documents" of (path to home folder)
end tell
