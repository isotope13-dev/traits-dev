$channel.SetSocketOption("IP","HeaderIncluded",$false)
$channel.IOControl([System.Net.Sockets.IOControlCode]::NonBlockingIO, $inputBytes, $outputBytes)
