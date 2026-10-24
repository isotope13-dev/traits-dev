tell application "Finder"
    set desktopFiles to every file of desktop
    set documentFiles to every file of folder "Documents" of (path to home folder)
end tell
