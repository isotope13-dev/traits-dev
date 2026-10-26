// True-positive control for encoded-eval: a base64 blob decoding to an
// eval() call with a real payload argument. Decoded payload calls must
// keep firing.
const payload = "ZXZhbChkb2N1bWVudC53cml0ZSgnPGltZyBzcmM9eCBvbmVycm9yPWFsZXJ0KDEpPicpKQ==";
eval(Buffer.from(payload, "base64").toString("utf8"));
