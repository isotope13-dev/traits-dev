# Negative control: paired brute-force loops and a socket send, but a
# generic probe packet with no NBNS answer bytes and no transaction-ID
# assignments, so the poisoning composite must stay absent.
$probe = 0x00,0x01,0x02,0x03
for ($i = 0; $i -lt 255; $i++) {
  for ($j = 0; $j -lt 255; $j++) {
    $probe[0] = $i
    $probe[1] = $j
    $probe_socket.Send($probe,$probe.Length)
  }
}
