# Synthetic staged poisoning: NBNS answer bytes, transaction-ID walk, and
# paired brute-force loops, but no socket send, so the delivery rule stays
# silent and only the staged form fires.
$NBNS_response_packet = 0x00,0x00,0x85,0x00,0x00,0x00,0x00,0x01
$k = 0
while ($k -lt 255) {
  $m = 0
  while ($m -lt 255) {
    $NBNS_response_packet[0] = $k
    $NBNS_response_packet[1] = $m
    $m++
  }
  $k++
}
