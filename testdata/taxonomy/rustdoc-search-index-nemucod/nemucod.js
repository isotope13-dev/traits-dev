var encoded = "104,116,116,112,115,58,47,47,101,120,97,109,112,108,101,46,105,110,118,97,108,105,100,47,112,97,121,108,111,97,100,46,101,120,101";
var decoded = encoded.split(",").map(function (c) { return String.fromCharCode(parseInt(c, 10)); }).join("");
console.log(decoded);
