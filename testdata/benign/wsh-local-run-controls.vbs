' Local helper launcher control: runs a local script with a normal window.
' No reversed names, no remote URL, so neither mshta/dropper conviction
' may fire.
Dim sh
Set sh = CreateObject("WScript.Shell")
sh.Run "wscript.exe helper.vbs", 1, False
Set sh = Nothing
