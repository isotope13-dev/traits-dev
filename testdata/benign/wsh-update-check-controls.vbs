' Benign update-check control: fetches a version string and prompts the user.
' The response is compared as data; nothing is executed and no string
' obfuscation is used, so this must never read as a download-and-execute
' dropper.
Dim http, current, latest
current = "1.4.2"
Set http = CreateObject("MSXML2.XMLHTTP")
http.open "GET", "https://updates.example.com/app/version.txt", False
http.send
If http.Status = 200 Then
    latest = Trim(http.responseText)
    If latest <> current Then
        MsgBox "Update available: " & latest
    End If
End If
Set http = Nothing
