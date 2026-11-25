# Synthetic control fixture: a local HTTP listener reads the request body and
# echoes a JSON status. It never decodes a payload or starts a child process.
$listener = [System.Net.HttpListener]::new()
$listener.Prefixes.Add('http://+:8765/')
$listener.Start()
while ($listener.IsListening) {
    $ctx = $listener.GetContext()
    $req = $ctx.Request
    $resp = $ctx.Response
    $sr = [IO.StreamReader]::new($req.InputStream, $req.ContentEncoding)
    $text = $sr.ReadToEnd()
    $out = [Text.Encoding]::UTF8.GetBytes('{"ok":true,"bytes":' + $text.Length + '}')
    $resp.OutputStream.Write($out, 0, $out.Length)
    $resp.OutputStream.Close()
}
