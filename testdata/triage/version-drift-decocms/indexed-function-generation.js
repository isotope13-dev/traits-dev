// Code generation and indexed constructor arguments are separate observations.
const strings = ["return 7", "return 8"];
const first = new Function(strings[0x0]);
const second = new Function(strings[0x1]);
const third = new Function(decodeSource());
first();
