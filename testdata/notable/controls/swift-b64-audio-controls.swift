import Foundation

// Voice-audio control mirroring the overturned shape: base64 decoding of
// realtime audio frames with no process execution anywhere nearby.
func decodeFrame(_ s: String) -> Data? {
  return Data(base64Encoded: s)
}
