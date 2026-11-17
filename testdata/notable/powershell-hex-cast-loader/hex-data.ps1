$hex = '0123456789abcdef'
for($pos=0;$pos -lt $hex.Length;$pos+=2){
    Write-Output ([int]('0x'+$hex.Substring($pos,2)))
}
