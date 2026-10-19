var character = String.fromCharCode;
var numbers = [80, 79, 78, 77];
var method = '';
for (var i = 0; i < numbers.length; i++) method += character(numbers[i] ^ 5);
target[method](1);
target[method](2);
target[method](3);
WScript.Sleep(10);
