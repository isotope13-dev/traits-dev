# Synthetic NBNS spoof loop: same Inveigh-family technique as the triaged
# relay skeleton (NBNS answer bytes, transaction-ID walk, paired brute-force
# loops, socket send) with renamed loop variables and a while-loop shape,
# but no NTLM relay or reflection half, so it must stay suspicious.
$NBNS_response_packet = 0x00,0x00,0x85,0x00,0x00,0x00,0x00,0x01
$a = 0
while ($a -lt 255) {
  $b = 0
  while ($b -lt 255) {
    $NBNS_response_packet[0] = $a
    $NBNS_response_packet[1] = $b
    $answer_socket.Send($NBNS_response_packet,$NBNS_response_packet.Length)
    $b++
  }
  $a++
}
