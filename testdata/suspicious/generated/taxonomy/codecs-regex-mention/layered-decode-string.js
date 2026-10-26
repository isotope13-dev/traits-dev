// Malicious control: layered base64-plus-codecs decoding in a string.
const payload = "import codecs;codecs.decode(b64decode(blob))";
