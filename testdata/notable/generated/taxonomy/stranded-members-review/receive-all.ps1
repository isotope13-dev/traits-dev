$channel.IOControl([System.Net.Sockets.IOControlCode]::ReceiveAll, $inputBytes, $outputBytes)
$channel.SetSocketOption("IP","HeaderIncluded",$true)
