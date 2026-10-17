// Benign control: decoder names inside a detection alternation string. The
// escaped `codecs\.` is regex source, not a layered-encoding call.
const DECODERS = "base64|b64decode|fromhex|codecs\\.decode|marshal\\.loads";
