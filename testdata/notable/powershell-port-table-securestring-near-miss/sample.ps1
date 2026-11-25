# Near miss: a port table and a SecureString conversion, no byte payload.
$script:NotWebPorts = @(21, 22, 25, 53, 110, 143, 465, 587, 993, 995, 1194, 1883, 3129, 3306, 4822,
    5432, 5900, 5901, 6379, 6881, 8883, 9300, 11211, 27017, 51413)
function Get-PlainText([Security.SecureString]$Secure) {
    $ptr = [Runtime.InteropServices.Marshal]::SecureStringToGlobalAllocUnicode($Secure)
    try { $chars = New-Object char[] $Secure.Length; [Runtime.InteropServices.Marshal]::Copy($ptr, $chars, 0, $Secure.Length); -join $chars }
    finally { [Runtime.InteropServices.Marshal]::ZeroFreeGlobalAllocUnicode($ptr) }
}
