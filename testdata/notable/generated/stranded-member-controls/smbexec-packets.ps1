# Minimal raw-SMB service-execution shape: Empire lateral function plus
# hand-built SVCCTL create/delete packets over an NTLMSSP session.
function Invoke-SMBExec {
  $a = 'NTLMSSP negotiate'
  $b = 'NTLMSSP authenticate'
}
function Get-PacketSCMCreateServiceW() { return $null }
function Get-PacketSCMDeleteServiceW() { return $null }
