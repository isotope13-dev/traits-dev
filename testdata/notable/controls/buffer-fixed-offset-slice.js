// Benign binary-record parser: carves fixed-offset fields out of a frame
// with subarray at hex offsets. Must resolve to the fixed-offset buffer
// slicing traits, never to a hostile verdict.
export function parseFrame(view) {
  const kind = view.subarray(0x0, 0x4);
  const seq = view.subarray(0x4, 0x8);
  const body = view.subarray(0x8, 0x20);
  return { kind, seq, body };
}
