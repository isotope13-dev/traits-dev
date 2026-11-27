$interop='Runtime.InteropServices.Marshal'
$native=[type]($interop)
$native::('Copy')($bytes,0,$destination,$bytes.Length)
