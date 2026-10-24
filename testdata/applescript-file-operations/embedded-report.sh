#!/bin/sh
osascript -e 'run script "set contentsRead to read sourceFile" & return & "set outputHandle to (open for access reportFile with write permission)" & return & "set eof of outputHandle to 0" & return & "write reportData to outputHandle starting at eof" & return & "close access outputHandle"'
