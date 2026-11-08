Set ol = CreateObject("Outlook.Application")
Set ns = ol.GetNamespace("MAPI")
Set fso = CreateObject("Scripting.FileSystemObject")
Set f = fso.CreateTextFile("C:\temp\gal.csv")
Set gal = ns.AddressLists(1)
For i = 1 To gal.AddressEntries.Count
  f.WriteLine gal.AddressEntries(i).Name & "," & gal.AddressEntries(i).Address
Next
f.Close
