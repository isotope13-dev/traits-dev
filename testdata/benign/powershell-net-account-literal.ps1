$Command = "net user newuser Pass123 /add; net localgroup administrators newuser /add"
Write-Output $Command
