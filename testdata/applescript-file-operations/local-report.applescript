-- Ordinary local file operations; no theft is implied.
set contentsRead to read sourceFile
set outputHandle to (open for access reportFile with write permission)
set eof of outputHandle to 0
write reportData to outputHandle starting at eof
close access outputHandle
