$listener = New-Object System.Net.HttpListener
$listener.Prefixes.Add('http://localhost:8080/')
$listener.Start()
$challenge = 'TlRMTVNTUAACAAAAAAAAAAAAAAAFgomiESIzRFVmd4gAAAAAAAAAAAAAAAAAAAAA'
for ($i = 0; $i -lt 4; $i++) {
    $context = $listener.GetContext()
    if ($context.Request.Headers['Authorization']) {
    }
    $context.Response.StatusCode = 401
    $context.Response.AddHeader('WWW-Authenticate', "NTLM $challenge")
    $context.Response.Close()
}
$listener.Stop()
