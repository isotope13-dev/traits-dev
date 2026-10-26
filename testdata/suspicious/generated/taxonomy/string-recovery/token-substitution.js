var firstTokens = ["A1", "B2", "C3", "D4", "E5", "F6"];
var secondTokens = ["G7", "H8", "I9", "J0", "K1", "L2"];
var flags = "gi";

function decode(input, pattern, replacement) {
  input = input.replace(new RegExp(pattern, flags), replacement);
  input = input.replace(new RegExp(replacement, flags), pattern);
  input = input["replace"](pattern, replacement);
  return input;
}
