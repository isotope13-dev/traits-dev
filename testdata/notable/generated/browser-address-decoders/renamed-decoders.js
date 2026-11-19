  function readAddress(input) {
    var alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz';
    if (input.length < 26 || input.length > 45) return null;
    var total = 0n, i, digit;
    for (i = 0; i < input.length; i++) {
      digit = alphabet.indexOf(input.charAt(i));
      if (digit < 0) return null;
      total = total * 58n + BigInt(digit);
    }
    var hex = total.toString(16);
    if (hex.length % 2) hex = '0' + hex;
    var bytes = [];
    for (i = 0; i < hex.length; i += 2) bytes.push(parseInt(hex.substr(i, 2), 16));
    for (i = 0; i < input.length && input.charAt(i) === '1'; i++) bytes.unshift(0);
    return bytes;
  }

  function readToken(input) {
    if (input.length !== 48) return null;
    var alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_';
    var bytes = [], remaining = 0, accumulator = 0, i, digit;
    for (i = 0; i < input.length; i++) {
      digit = alphabet.indexOf(input.charAt(i));
      if (digit < 0) return null;
      accumulator = (accumulator << 6) | digit;
      remaining += 6;
      if (remaining >= 8) { remaining -= 8; bytes.push((accumulator >> remaining) & 0xff); }
    }
    return bytes;
  }

