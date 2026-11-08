Set ol = CreateObject("Outlook.Application")
Set mail = ol.CreateItem(0)
mail.Recipients.Add "finance@example.com"
mail.Subject = "Q3 report"
mail.Attachments.Add "C:\reports\q3.xlsx"
mail.Send
