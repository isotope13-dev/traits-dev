const bytes = [100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115];
let code = ""; for (let i = 0; i < bytes.length; i++) code += String.fromCharCode(bytes[i] ^ 7);
eval(code);
