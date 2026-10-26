package service

// WebSocket frame unmasking (RFC 6455, section 5.3): the masking key
// supplied in the frame header is XORed over the payload octets. This is
// transport decoding applied to every client-to-server frame, not an
// obfuscated-payload decode loop.
func unmaskFrame(payload []byte, mask [4]byte) {
	for i := range payload {
		payload[i] ^= mask[i%4]
	}
}
