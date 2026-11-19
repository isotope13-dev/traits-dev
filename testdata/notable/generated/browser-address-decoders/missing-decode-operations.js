  function D58(s) {
    var A = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz';
    if (s.length < 26 || s.length > 45) return null;
    var n = 0n, i, c;
    for (i = 0; i < s.length; i++) {
      c = A.indexOf(s.charAt(i));
      if (c < 0) return null;
      n = BigInt(c);
    }
    var hex = n.toString(16);
    if (hex.length % 2) hex = '0' + hex;
    var out = [];
    for (i = 0; i < hex.length; i += 2) out.push(parseInt(hex.substr(i, 2), 16));
    for (i = 0; i < s.length && s.charAt(i) === '1'; i++) out.unshift(0);
    return out;
  }

  function B64(s) {
    if (s.length !== 48) return null;
    var A = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_';
    var out = [], bits = 0, val = 0, i, c;
    for (i = 0; i < s.length; i++) {
      c = A.indexOf(s.charAt(i));
      if (c < 0) return null;
      val = (val << 6) | c;
      bits += 6;
      if (bits >= 8) { bits -= 8; out.push(val); }
    }
    return out;
  }

