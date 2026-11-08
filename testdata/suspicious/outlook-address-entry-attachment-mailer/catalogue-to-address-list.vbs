Set ol = CreateObject("Outlook.Application")
Set ns = ol.GetNamespace("MAPI")
Set lst = ns.AddressLists("Customers")
For i = 1 To lst.AddressEntries.Count
  Set mail = ol.CreateItem(0)
  mail.Recipients.Add lst.AddressEntries(i).Address
  mail.Subject = "Spring catalogue"
  mail.Attachments.Add "C:\marketing\catalogue.pdf"
  mail.Send
Next
