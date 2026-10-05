$bytes=[System.IO.File]::ReadAllBytes('report.bin')
for($offset=0;$offset -lt $bytes.Length;$offset+=192){[System.Console]::WriteLine([System.Convert]::ToBase64String($bytes,$offset,[Math]::Min(192,$bytes.Length-$offset)))}
