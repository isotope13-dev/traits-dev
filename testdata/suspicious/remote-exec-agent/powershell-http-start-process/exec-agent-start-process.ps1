# Synthetic regression fixture: HTTP listener hands a posted script to a child
# powershell.exe through Start-Process. No bearer check is shown, so the sample
# is only suspicious.
$listener = [System.Net.HttpListener]::new()
$listener.Prefixes.Add('http://+:8765/')
$listener.Start()
while ($listener.IsListening) {
    $ctx = $listener.GetContext()
    $req = $ctx.Request
    $resp = $ctx.Response
    $sr = [IO.StreamReader]::new($req.InputStream, $req.ContentEncoding)
    $body = $sr.ReadToEnd() | ConvertFrom-Json
    $scriptB64 = $body.script
    $bytes = [Convert]::FromBase64String($scriptB64)
    $file = Join-Path $env:TEMP ([Guid]::NewGuid().ToString('N') + '.ps1')
    [IO.File]::WriteAllBytes($file, $bytes)
    $proc = Start-Process -FilePath 'powershell.exe' -ArgumentList ('-NoProfile -ExecutionPolicy Bypass -File "' + $file + '"') -Wait -PassThru
    $out = [Text.Encoding]::UTF8.GetBytes("exit=" + $proc.ExitCode)
    $resp.OutputStream.Write($out, 0, $out.Length)
    $resp.OutputStream.Close()
}
