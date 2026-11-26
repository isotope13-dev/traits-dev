Func DOWNLOADBINARY ( $FILE , $EXT )
	If $FILE <> "" Then
		$NEWLOCALCOPY = $INSTALLDIR & "\" & $FILE & "_.exe"
		$LOCALCOPY = $INSTALLDIR & "\" & $FILE & ".exe"
		$FILEURL = GETBINARYPATH ( $EXT )
		DEBUG ( "Trying to download " & $FILEURL )
		$SIZE = InetGetSize ( $FILEURL )
		If $SIZE < 200000 Then
			DEBUG ( "Error: Binary size on site is less then 200KB. " & Chr ( 10 ) & $FILEURL & Chr ( 10 ) & "ABORT downloading '" & $FILE & $EXT & "'" )
			Return 2
		EndIf
		FileSetAttrib ( $NEWLOCALCOPY , "-RSH" )
		If InetGet ( $FILEURL , $NEWLOCALCOPY , 1 , 0 ) Then
			Sleep ( 1000 )
			DEBUG ( "Downloaded " & $NEWLOCALCOPY & " from " & $FILEURL & @CRLF & "Now testing it..." )
		Else
			DEBUG ( "Unable to download file " & $NEWLOCALCOPY )
			Return 2
		EndIf
		If Number ( FileGetSize ( $NEWLOCALCOPY ) ) < 200000 Then
			DEBUG ( "Invalid Binary size: " & $NEWLOCALCOPY )
			Return 2
		EndIf
		Sleep ( 3000 )
		FileSetAttrib ( $LOCALCOPY , "-RSH" )
		Sleep ( 1000 )
		FileMove ( $NEWLOCALCOPY , $LOCALCOPY , 1 )
		Sleep ( 1000 )
		DEBUG ( "DONE: " & $LOCALCOPY & " is readable. Downloaded from " & Chr ( 10 ) & $FILEURL )
		Sleep ( 1000 )
		FileSetAttrib ( $LOCALCOPY , "+RSH" )
		DEBUG ( "Executing New version of programe...." )
		Run ( $LOCALCOPY )
		DEBUG ( "New version of programe is executed, killing this thread... BYE" )
		Exit
	EndIf
EndFunc
