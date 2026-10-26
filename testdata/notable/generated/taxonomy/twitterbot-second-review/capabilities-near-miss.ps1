$p = New-Object System.Diagnostics.ProcessStartInfo
$s.AcceptTcpListener()
$p.RedirectStandardInput = 0
$a = [AppDomain]::CreateDomain('isolated')
$a.DefineDynamicAssembly($n, $access)
$program = 'rundll64.exe'
$url = 'http://api.twitter.com/1/statuses/update.xml'

