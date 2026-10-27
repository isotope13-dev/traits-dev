function xorCodec(input, key) {
  let output = "";
  for (let i = 0; i < input.length; i++) {
    output += String.fromCharCode(input.charCodeAt(i) ^ key.charCodeAt(i % key.length));
  }
  return output;
}
console.log(xorCodec("abc", "k"));
const expression = "40+2";
console.log(eval(expression));
