osascript -e 'run script "" & return & "do shell script \"mkdir -p \" & quotedPath" & return & "set kind to (do shell script \"file -b \" & quotedPath)"'
