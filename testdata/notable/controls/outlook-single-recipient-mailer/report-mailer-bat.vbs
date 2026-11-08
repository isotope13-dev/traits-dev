' Sends the nightly build log batch to ops
Set ol = CreateObject("Outlook.Application")
Set mail = ol.CreateItem(0)
mail.Recipients.Add "ops@example.com"
mail.Attachments.Add "C:\build\deploy.bat"
mail.Send
