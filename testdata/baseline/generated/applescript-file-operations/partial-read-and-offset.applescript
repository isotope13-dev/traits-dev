-- These operations do not prove an unbounded read or truncation to zero.
set headerData to read sourceFile for 16
set eof of outputHandle to 0 + retainedBytes
write reportData to outputHandle starting at eof + 1
open for access sourceFile
