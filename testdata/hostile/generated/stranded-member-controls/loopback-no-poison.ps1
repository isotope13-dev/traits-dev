function SMBRelayExecute { param($socket, $user) }
$challenge = "NTLMSSP challenge"
$authenticate = "NTLMSSP authenticate"
$SMBRelayTarget = "127.0.0.1"
$SMB_relay_command += "{0:X2}-00-"
$NBNS_response_packet = 0x00,0x00,0x85,0x00,0x00,0x00,0x00,0x01
for ($i = 0; $i -lt 255; $i++) {
 for ($j = 0; $j -lt 255; $j++) {
  $NBNS_response_packet[0] = $i
  $NBNS_response_packet[1] = $j
 }
}
