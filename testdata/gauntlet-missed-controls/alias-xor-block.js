const character = String.fromCharCode;
const input = [80, 79, 78, 77];
let output = '';
for (let index = 0; index < input.length; index++) {
    output += character(input[index] ^ 5);
}
