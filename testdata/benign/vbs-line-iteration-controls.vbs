' Line-iteration control: walks a vbCrLf-split server list and shows each.
' The Split iterates lines, so the path-list atom still fires here, while
' no decoder or dynamic executor may appear.
Dim hosts, h
hosts = "server1" & vbCrLf & "server2"
For Each h In Split(hosts, vbCrLf)
  If h <> "" Then MsgBox h
Next
