// Packed loader: a numeric char-code payload is decoded and evaluated.
var payload = [118, 97, 114, 32, 120, 61, 49, 59, 32, 99, 111, 110, 115, 111, 108, 101, 46, 108, 111, 103, 40, 120, 41, 59, 32, 97, 108, 101, 114, 116, 40, 49, 41, 59, 32, 100, 111, 99, 117, 109, 101, 110, 116, 46, 119, 114, 105, 116, 101, 40, 39, 111, 107, 39, 41, 59];
var code = String.fromCharCode.apply(null, payload);
eval(code);
