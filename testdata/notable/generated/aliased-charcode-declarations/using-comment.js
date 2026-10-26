using/* resource */decode = String.fromCharCode;
for (let i=0; i<bytes.length; i++) { output += decode(bytes[i] ^ 23); }
